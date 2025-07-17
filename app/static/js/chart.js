// static/js/chart.js

class ParkingCharts {
  constructor() {
    // Chart.js instances
    this.revenueChart   = null;
    this.occupancyChart = null;
    // Kick things off
    document.addEventListener('DOMContentLoaded', () => this.init());
  }

  async init() {
    // Pick the correct endpoint
    const dataUrl = window.LOT_ANALYTICS_DATA_URL || '/admin/analytics/data';

    try {
      const res  = await fetch(dataUrl, { credentials: 'same-origin' });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const json = await res.json();

      if (window.LOT_ANALYTICS_DATA_URL) {
        // Single‑lot analytics
        this.renderSingleLot(json);
      } else {
        // Multi‑lot analytics
        this.renderMultiLot(json);
      }

    } catch (err) {
      console.error('Could not fetch analytics data:', err);
      // show fallback messages
      this.showNoData('revenueChart',   'Could not load revenue data.');
      this.showNoData('occupancyChart', 'Could not load occupancy data.');
    }
  }

  // ───── Single‑lot ─────
  renderSingleLot({ lot, revenue, occupied, total }) {
    // Revenue
    if (+revenue > 0) {
      this.drawBar('revenueChart', [lot], [+revenue], 'Total Revenue (₹)');
    } else {
      this.showNoData('revenueChart', 'No revenue yet.');
    }

    // Occupancy
    const pct = total>0 ? (occupied/total)*100 : 0;
    if (pct > 0) {
      this.drawDoughnut(
        'occupancyChart',
        ['Occupied','Free'],
        [pct, 100-pct]
      );
    } else {
      this.showNoData('occupancyChart', 'No cars parked yet.');
    }
  }

  // ───── Multi‑lot ─────
  renderMultiLot({ revenue: revArr, occupancy: occArr }) {
    const revenueData   = Array.isArray(revArr) ? revArr : [];
    const occupancyData = Array.isArray(occArr) ? occArr : [];

    // Revenue chart or fallback
    if (revenueData.length) {
      const labels = revenueData.map(d => d.lot);
      const values = revenueData.map(d => +d.revenue);
      this.drawBar('revenueChart', labels, values, 'Total Revenue (₹)');
    } else {
      this.showNoData('revenueChart', 'No revenue data available.');
    }

    // Occupancy chart or fallback
    if (occupancyData.length) {
      const labels  = occupancyData.map(d => d.lot);
      const percents = occupancyData.map(d => {
        const occ = +d.occupied, tot = +d.total||1;
        return tot>0 ? (occ/tot)*100 : 0;
      });
      const totalPct = percents.reduce((a,b)=>a+b,0);
      if (totalPct>0) {
        this.drawDoughnut('occupancyChart', labels, percents);
      } else {
        this.showNoData('occupancyChart', 'No cars have parked yet.');
      }
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
      data: {
        labels,
        datasets: [{
          label: datasetLabel,
          data,
          borderRadius: 4,
          maxBarThickness: 80
        }]
      },
      options: {
        plugins: { legend: { display: false } },
        scales: {
          y: { beginAtZero: true, ticks: { callback: v => `₹${v}` } },
          x: { grid: { display: false } }
        }
      }
    });
  }

  drawDoughnut(canvasId, labels, data) {
    const ctx = document.getElementById(canvasId);
    if (this[canvasId]) this[canvasId].destroy();

    this[canvasId] = new Chart(ctx, {
      type: 'doughnut',
      data: { labels, datasets:[{ data }] },
      options: { plugins: { legend:{ position:'bottom' } }, cutout:'70%' }
    });
  }

  showNoData(canvasId, message) {
    const canvas = document.getElementById(canvasId);
    const div    = document.createElement('div');
    div.className = 'text-center text-muted mt-4';
    div.textContent = message;
    canvas.parentNode.replaceChild(div, canvas);
  }
}

// Instantiate it
new ParkingCharts();
