/**
 * LeetCode Solutions Archive — Frontend Logic
 * Fetches solutions.json → renders stats cards + searchable/filterable table
 */

'use strict';

// ── State ──────────────────────────────────────────────────────────────────
let allSolutions = [];
let filtered = [];
let activeFilter = 'all';   // 'all' | 'Easy' | 'Medium' | 'Hard'
let sortKey = 'id';
let sortDir = 'asc';

// ── Init ───────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  fetch('solutions.json')
    .then(r => {
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return r.json();
    })
    .then(data => {
      allSolutions = Array.isArray(data) ? data : [];
      applyFilter('all');
      renderStats();
    })
    .catch(err => {
      console.error('Failed to load solutions.json:', err);
      showState('error', '⚠️ Could not load solution data.', 'Make sure solutions.json exists in the Web/ folder.');
    });

  // Search
  const searchInput = document.getElementById('searchInput');
  if (searchInput) {
    let debounce;
    searchInput.addEventListener('input', () => {
      clearTimeout(debounce);
      debounce = setTimeout(filterAndRender, 250);
    });
  }

  // Scroll-to-top button
  const scrollBtn = document.getElementById('scroll-top');
  if (scrollBtn) {
    window.addEventListener('scroll', () => {
      scrollBtn.classList.toggle('visible', window.scrollY > 320);
    });
    scrollBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  }

  // Column sort headers
  document.querySelectorAll('[data-sort]').forEach(th => {
    th.addEventListener('click', () => handleSort(th.dataset.sort));
  });
});

// ── Filter ─────────────────────────────────────────────────────────────────
function applyFilter(diff) {
  activeFilter = diff;

  // Update button states
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.classList.remove('active');
    if (btn.dataset.diff === diff) btn.classList.add('active');
  });

  filterAndRender();
}

function filterAndRender() {
  const q = (document.getElementById('searchInput')?.value || '').toLowerCase().trim();

  filtered = allSolutions.filter(p => {
    const diffMatch =
      activeFilter === 'all' || p.difficulty === activeFilter;

    const textMatch =
      !q ||
      String(p.id).includes(q) ||
      p.name.toLowerCase().includes(q) ||
      (p.difficulty || '').toLowerCase().includes(q) ||
      (p.language || '').toLowerCase().includes(q) ||
      (p.slug || '').toLowerCase().includes(q);

    return diffMatch && textMatch;
  });

  sortData();
  renderTable(filtered);

  const count = document.getElementById('result-count');
  if (count) {
    count.textContent = `${filtered.length} of ${allSolutions.length} problems`;
  }
}

// ── Sort ───────────────────────────────────────────────────────────────────
function handleSort(key) {
  if (sortKey === key) {
    sortDir = sortDir === 'asc' ? 'desc' : 'asc';
  } else {
    sortKey = key;
    sortDir = 'asc';
  }

  // Update header icons
  document.querySelectorAll('[data-sort]').forEach(th => {
    th.classList.remove('sorted');
    const icon = th.querySelector('.sort-icon');
    if (icon) icon.textContent = '↕';
  });
  const activeTh = document.querySelector(`[data-sort="${key}"]`);
  if (activeTh) {
    activeTh.classList.add('sorted');
    const icon = activeTh.querySelector('.sort-icon');
    if (icon) icon.textContent = sortDir === 'asc' ? '↑' : '↓';
  }

  sortData();
  renderTable(filtered);
}

function sortData() {
  const DIFF_ORDER = { Easy: 0, Medium: 1, Hard: 2, Unknown: 3 };
  filtered.sort((a, b) => {
    let va, vb;
    switch (sortKey) {
      case 'id':
        va = a.id; vb = b.id;
        return sortDir === 'asc' ? va - vb : vb - va;
      case 'difficulty':
        va = DIFF_ORDER[a.difficulty] ?? 99;
        vb = DIFF_ORDER[b.difficulty] ?? 99;
        return sortDir === 'asc' ? va - vb : vb - va;
      case 'name':
        return sortDir === 'asc'
          ? a.name.localeCompare(b.name)
          : b.name.localeCompare(a.name);
      default:
        return 0;
    }
  });
}

// ── Stats ──────────────────────────────────────────────────────────────────
function renderStats() {
  const total  = allSolutions.length;
  const easy   = allSolutions.filter(p => p.difficulty === 'Easy').length;
  const medium = allSolutions.filter(p => p.difficulty === 'Medium').length;
  const hard   = allSolutions.filter(p => p.difficulty === 'Hard').length;

  setText('stat-total',  total);
  setText('stat-easy',   easy);
  setText('stat-medium', medium);
  setText('stat-hard',   hard);
}

// ── Render Table ───────────────────────────────────────────────────────────
function renderTable(data) {
  const tbody = document.getElementById('solutions-body');
  if (!tbody) return;

  if (data.length === 0) {
    tbody.innerHTML = `
      <tr><td colspan="6">
        <div class="state-msg">
          <span class="icon">🔍</span>
          No problems match your search.
        </div>
      </td></tr>`;
    return;
  }

  tbody.innerHTML = data.map(p => {
    const diffClass = {
      Easy: 'diff-easy',
      Medium: 'diff-medium',
      Hard: 'diff-hard',
    }[p.difficulty] || 'diff-unknown';

    const lcLink  = p.lc_link  || `https://leetcode.com/problems/${p.slug}/`;
    const solLink = p.sol_link || '#';

    return `
      <tr>
        <td class="prob-id">${p.id}</td>
        <td class="prob-name">${escHtml(p.name)}</td>
        <td><span class="diff-badge ${diffClass}">${escHtml(p.difficulty || 'Unknown')}</span></td>
        <td><span class="lang-badge">${escHtml(p.language || '')}</span></td>
        <td>
          <div class="action-cell">
            <a href="${escHtml(lcLink)}"  target="_blank" rel="noopener" class="btn-action btn-problem">
              ${svgExternal()} Problem
            </a>
            <a href="${escHtml(solLink)}" target="_blank" rel="noopener" class="btn-action btn-solution">
              ${svgCode()} Solution
            </a>
          </div>
        </td>
      </tr>`;
  }).join('');
}

// ── Helpers ────────────────────────────────────────────────────────────────
function showState(type, heading, msg = '') {
  const tbody = document.getElementById('solutions-body');
  if (tbody) {
    tbody.innerHTML = `
      <tr><td colspan="6">
        <div class="state-msg">
          <span class="icon">${type === 'error' ? '⚠️' : '⏳'}</span>
          <strong>${heading}</strong><br>${msg}
        </div>
      </td></tr>`;
  }
}

function setText(id, val) {
  const el = document.getElementById(id);
  if (el) el.textContent = val;
}

function escHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function svgCode() {
  return `<svg viewBox="0 0 16 16"><path d="M4.72 3.22a.75.75 0 0 1 1.06 1.06L2.56 7.5l3.22 3.22a.75.75 0 1 1-1.06 1.06L.97 8.03a.75.75 0 0 1 0-1.06l3.75-3.75zm6.56 0a.75.75 0 0 0-1.06 1.06L13.44 7.5l-3.22 3.22a.75.75 0 1 0 1.06 1.06l3.75-3.75a.75.75 0 0 0 0-1.06l-3.75-3.75z"/></svg>`;
}

function svgExternal() {
  return `<svg viewBox="0 0 16 16"><path d="M3.75 2h3.5a.75.75 0 0 1 0 1.5h-3.5a.25.25 0 0 0-.25.25v8.5c0 .138.112.25.25.25h8.5a.25.25 0 0 0 .25-.25v-3.5a.75.75 0 0 1 1.5 0v3.5A1.75 1.75 0 0 1 12.25 14h-8.5A1.75 1.75 0 0 1 2 12.25v-8.5C2 2.784 2.784 2 3.75 2zm6.854-1h4.146a.25.25 0 0 1 .25.25v4.146a.25.25 0 0 1-.427.177L13.03 4.03 9.28 7.78a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042l3.75-3.75-1.543-1.543A.25.25 0 0 1 10.604 1z"/></svg>`;
}
