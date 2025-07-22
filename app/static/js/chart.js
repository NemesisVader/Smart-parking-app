// static/js/chart.js

class ParkingCharts {
  constructor() {
    this.revenueChart = null;
    this.occupancyChart = null;
    document.addEventListener('DOMContentLoaded', () => this.init());
  }

  async init() {
    const dataUrl = window.LOT_ANALYTICS_DATA_URL || '/admin/analytics/data';

    try {
      const res = await fetch(dataUrl, { credentials: 'same-origin' });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const json = await res.json();

      if (window.LOT_ANALYTICS_DATA_URL) {
        this.renderSingleLot(json);
      } else {
        this.renderMultiLot(json);
      }

    } catch (err) {
      console.error('Could not fetch analytics data:', err);
      this.showNoData('revenueChart', 'Could not load revenue data.');
      this.showNoData('occupancyChart', 'Could not load occupancy data.');
    }
  }

  // ───── Single‑lot ─────
  renderSingleLot(json) {
    // extract single-lot objects from arrays
    const revObj = Array.isArray(json.revenue) ? json.revenue[0] : json.revenue;
    const occObj = Array.isArray(json.occupancy) ? json.occupancy[0] : json.occupancy;

    // Revenue
    const revenueValue = +revObj.revenue || 0;
    if (revenueValue > 0) {
      this.drawBar('revenueChart', [revObj.lot], [revenueValue], 'Total Revenue (₹)');
    } else {
      this.showNoData('revenueChart', 'No revenue yet.');
    }

    // Occupancy
    const occupied = +occObj.occupied || 0;
    const total = +occObj.total || 0;
    if (total > 0) {
      this.drawDoughnut(
        'occupancyChart',
        ['Occupied', 'Available'],
        [occupied, total - occupied]
      );
    } else {
      this.showNoData('occupancyChart', 'No occupancy data available.');
    }
  }

  // ───── Multi‑lot ─────
  renderMultiLot({ revenue: revArr, occupancy: occArr }) {
    const revenueData = Array.isArray(revArr) ? revArr : [];
    const occupancyData = Array.isArray(occArr) ? occArr : [];

    if (revenueData.length) {
      const labels = revenueData.map(d => d.lot);
      const values = revenueData.map(d => +d.revenue);
      this.drawBar('revenueChart', labels, values, 'Total Revenue (₹)');
    } else {
      this.showNoData('revenueChart', 'No revenue data available.');
    }

    if (occupancyData.length) {
      const labels = occupancyData.map(d => d.lot);
      const data = occupancyData.map(d => +d.occupied);
      const total = occupancyData.map(d => +d.total);
      const available = total.map((t, i) => t - data[i]);
      const combined = [];
      for (let i = 0; i < labels.length; i++) {
        // draw separate charts if needed; here we sum
        combined.push([labels[i], data[i], available[i]]);
      }
      // For multi, fallback to single-lot style for each lot
      this.drawDoughnut(
        'occupancyChart',
        ['Occupied','Available'],
        [data.reduce((a,b)=>a+b,0), available.reduce((a,b)=>a+b,0)]
      );
    } else {
      this.showNoData('occupancyChart', 'No occupancy data available.');
    }
  }

  // ───── Drawing Helpers ─────
  drawBar(canvasId, labels, data, datasetLabel) {
    const ctx = document.getElementById(canvasId);
    if (this[canvasId]) this[canvasId].destroy();

    this[canvasId] = new Chart(ctx, {
      type: 'bar',
      data: { labels, datasets: [{ label: datasetLabel, data, borderRadius: 4, maxBarThickness: 80 }] },
      options: { plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, ticks: { callback: v => `₹${v}` } }, x: { grid: { display: false } } } }
    });
  }

  drawDoughnut(canvasId, labels, data) {
    const ctx = document.getElementById(canvasId);
    if (this[canvasId]) this[canvasId].destroy();

    this[canvasId] = new Chart(ctx, {
      type: 'doughnut',
      data: { labels, datasets: [{ data }] },
      options: { plugins: { legend: { position: 'bottom' } }, cutout: '70%' }
    });
  }

  showNoData(canvasId, message) {
    const canvas = document.getElementById(canvasId);
    const div = document.createElement('div');
    div.className = 'text-center text-muted mt-4';
    div.textContent = message;
    canvas.parentNode.replaceChild(div, canvas);
  }
}

new ParkingCharts();
