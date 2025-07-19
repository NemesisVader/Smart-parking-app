// === Replace with your actual Mapbox Access Token ===
mapboxgl.accessToken = 'pk.eyJ1Ijoia3J5cHRvdiIsImEiOiJjbWRhOW4xdXMwZXZrMmtzYjNqcDkwZWRqIn0.y8mkMofee6LCGMvV4T_zyQ';

const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v12',
    center: [78.9629, 20.5937], // Default to India center
    zoom: 5
});

const lotData = window.lotData || [];
let markers = [];

// === 1. Add current user location and nearby lots ===
navigator.geolocation.getCurrentPosition(pos => {
    const userCoords = [pos.coords.longitude, pos.coords.latitude];
    map.flyTo({ center: userCoords, zoom: 13 });

    new mapboxgl.Marker({ color: 'blue' })
        .setLngLat(userCoords)
        .setPopup(new mapboxgl.Popup().setText('Your Location'))
        .addTo(map);

    loadNearbyLots(userCoords);
}, () => {
    console.warn("User location not found. Showing all lots.");
    loadNearbyLots();
});

function clearMarkers() {
    markers.forEach(m => m.remove());
    markers = [];
}

function loadNearbyLots(center = null) {
    clearMarkers();

    const filteredLots = lotData
        .filter(lot => lot.lat && lot.lng)
        .map(lot => {
            const dx = lot.lng - (center?.[0] || lot.lng);
            const dy = lot.lat - (center?.[1] || lot.lat);
            const distance = Math.sqrt(dx * dx + dy * dy);
            console.log(`${lot.location_name} is ${distance.toFixed(3)}° away`);
            return { ...lot, distance };
        })
        .filter(lot => lot.distance < 0.5) // increased radius to ~50km
        .sort((a, b) => a.distance - b.distance)
        .slice(0, 5);

    renderLots(filteredLots);
}

// === 3. Render list and markers ===
function renderLots(lots) {
    const lotList = document.getElementById('lotList');
    lotList.innerHTML = '';

    if (lots.length === 0) {
        lotList.innerHTML = '<p class="text-muted">No Matching Lots Found</p>';
        return;
    }

    lots.forEach(lot => {
        const { lat, lng, location_name, address, id } = lot;

        const marker = new mapboxgl.Marker()
            .setLngLat([lng, lat])
            .setPopup(new mapboxgl.Popup().setHTML(`<b>${location_name}</b><br>${address}`))
            .addTo(map);
        markers.push(marker);

        const item = document.createElement('a');
        item.href = '#';
        item.className = 'list-group-item list-group-item-action';
        item.dataset.lotId = id;
        item.innerHTML = `<strong>${location_name}</strong><br><small>${address}</small>`;
        lotList.appendChild(item);
    });

    if (lots[0]) {
        map.flyTo({ center: [lots[0].lng, lots[0].lat], zoom: 13 });
    }
}

let searchMarker = null;

document.getElementById('searchInput').addEventListener('change', async (e) => {
    const query = e.target.value.trim();
    if (!query) return;

    const coords = await getCoordsFromMapbox(query);
    if (coords) {
        // Add red marker for search location
        if (searchMarker) searchMarker.remove();
        searchMarker = new mapboxgl.Marker({ color: 'red' })
            .setLngLat(coords)
            .setPopup(new mapboxgl.Popup().setText('Search Location'))
            .addTo(map);

        map.flyTo({ center: coords, zoom: 13 });
        loadNearbyLots(coords); // load markers for lots only
    } else {
        alert("Location not found.");
    }
});

async function getCoordsFromMapbox(query) {
    const token = mapboxgl.accessToken;
    const url = `https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(query)}.json?access_token=${token}&limit=1`;

    try {
        const res = await fetch(url);
        const data = await res.json();
        if (data.features && data.features.length > 0) {
            const [lng, lat] = data.features[0].center;
            return [lng, lat];
        }
    } catch (err) {
        console.error("Mapbox Geocoding failed:", err);
    }

    return null;
}
