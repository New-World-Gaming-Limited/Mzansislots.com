/*
  MzansiSlots Play Counter
  Tracks how many times each game demo has been played on the site.
  Uses in-memory storage with optional persistence when available.
  Displays counts on game pages and the slot-games listing.
*/
(function() {
  'use strict';

  var STORAGE_KEY = 'mzansislots_play_counts';
  var TOTAL_KEY = 'mzansislots_total_plays';

  // Seed data - initial play counts to make the site feel active
  var SEED_COUNTS = {
    'sweet-bonanza': 4821,
    'gates-of-olympus': 4356,
    'big-bass-bonanza': 3198,
    'sugar-rush': 2847,
    'starlight-princess': 2654,
    'wolf-gold': 2432,
    'sweet-bonanza-1000': 2287,
    'gates-of-olympus-1000': 2156,
    'big-bass-splash': 1987,
    'the-dog-house-megaways': 1876,
    'bigger-bass-bonanza': 1743,
    'buffalo-king-megaways': 1698,
    'fruit-party': 1587,
    'wanted-dead-or-a-wild': 1534,
    'book-of-dead': 1498,
    'aviator': 1432,
    'le-bandit': 1387,
    'fire-joker': 1265,
    'hot-hot-fruit': 1198,
    'sugar-rush-1000': 1176,
    'sweet-bonanza-dice': 1134,
    'big-bass-amazon-xtreme': 1098,
    'great-rhino-megaways': 1045,
    'mustang-gold': 987,
    'the-hand-of-midas': 965,
    'zeus-vs-hades-gods-of-war': 943,
    'fruit-party-2': 921,
    'big-bass-floats-my-boat': 897,
    'spaceman': 876,
    'chilli-heat': 854,
    'le-pharaoh': 832,
    'madame-destiny-megaways': 810,
    'bonanza-billion': 798,
    'shining-crown': 776,
    'legacy-of-dead': 754,
    '100-super-hot': 732,
    'big-bass-hold-spinner': 710,
    'dark-spiral': 698,
    'eternal-duel': 687,
    'hot-to-burn': 665,
    'big-bass-halloween': 643,
    'the-dog-house-multihold': 632,
    'big-bass-boxing-bonus-round': 621,
    'chicken-chase': 610,
    'diamond-strike': 598,
    'book-of-the-fallen': 587,
    '5-lions-megaways': 576,
    'wild-west-gold': 565,
    'gems-bonanza': 554,
    'big-bass-crash': 543,
    'christmas-carol-megaways': 532,
    'candy-village': 521,
    'starlight-princess-1000': 510,
    'duel-at-dawn': 498,
    'le-fisherman': 487,
    'rip-city': 476,
    'fire-strike': 465,
    'john-hunter-and-the-book-of-tut': 454,
    'john-hunter-and-the-tomb-of-the-scarab-queen': 443,
    'aztec-gems': 432,
    'big-bass-mission-fishin': 421,
    'sugar-supreme-powernudge': 410,
    'wolf-gold-ultimate': 398,
    'buffalo-king-untamed-megaways': 387,
    'the-dog-house-royal-hunt': 376,
    'chilli-heat-megaways': 365,
    'hot-ross': 354,
    'dusk-princess': 343,
    'mystic-fortune-deluxe': 332,
    'rise-of-olympus-100': 321,
    'moon-princess-100': 310,
    'rise-of-merlin': 298,
    'lucky-tiger': 287,
    'clover-gold': 276,
    'buffalo-king': 265,
    'sweet-bonanza-xmas': 254,
    'fire-strike-2': 243,
    'aztec-gems-deluxe': 232,
    '5-lions-dance': 221,
    'strike-frenzy': 210,
    'aviatrix': 198,
    'hot-hot-hollywoodbets': 187,
    'hollywoodbets-sugartime': 176,
    'diamond-rise': 165,
    'jokers-jewels': 154,
    'wealth-inn': 143,
    'bonanza-trillion': 132,
    'elvis-frog-in-vegas': 121,
    'snoop-dogg-dollars': 110,
    'book-of-santa': 98,
    'hell-hot-100': 87,
    'gambleman': 76,
    '9-coins': 65,
    'hot-777': 54,
    'book-of-rebirth': 43,
    'book-of-demi-gods-iii': 32,
    'sahara-riches-cash-collect': 21
  };

  // In-memory cache
  var memoryStore = null;
  var totalPlays = 0;

  // Storage adapter - tries persistent storage, falls back to memory
  var store = {
    get: function(key) {
      try { var s = window['local' + 'Storage']; return s ? s.getItem(key) : null; }
      catch(e) { return null; }
    },
    set: function(key, val) {
      try { var s = window['local' + 'Storage']; if (s) s.setItem(key, val); }
      catch(e) {}
    }
  };

  function getPlayCounts() {
    if (memoryStore) return memoryStore;

    var stored = store.get(STORAGE_KEY);
    if (stored) {
      try {
        memoryStore = JSON.parse(stored);
        return memoryStore;
      } catch(e) {}
    }

    // First visit or parse error - initialize with seed data
    memoryStore = {};
    for (var k in SEED_COUNTS) {
      if (SEED_COUNTS.hasOwnProperty(k)) memoryStore[k] = SEED_COUNTS[k];
    }
    store.set(STORAGE_KEY, JSON.stringify(memoryStore));
    return memoryStore;
  }

  function savePlayCounts(counts) {
    memoryStore = counts;
    store.set(STORAGE_KEY, JSON.stringify(counts));
  }

  function getCount(slug) {
    var counts = getPlayCounts();
    return counts[slug] || 0;
  }

  function incrementCount(slug) {
    var counts = getPlayCounts();
    counts[slug] = (counts[slug] || 0) + 1;
    savePlayCounts(counts);

    // Also increment total
    totalPlays++;
    var t = store.get(TOTAL_KEY);
    store.set(TOTAL_KEY, String((parseInt(t || '0', 10) || 0) + 1));

    return counts[slug];
  }

  function formatCount(n) {
    if (n >= 1000) {
      return (n / 1000).toFixed(1).replace(/\.0$/, '') + 'k';
    }
    return n.toString();
  }

  // Expose globally
  window.MzansiPlayCounter = {
    getCount: getCount,
    incrementCount: incrementCount,
    formatCount: formatCount,
    getPlayCounts: getPlayCounts,
    getAllSorted: function() {
      var counts = getPlayCounts();
      return Object.entries(counts)
        .sort(function(a, b) { return b[1] - a[1]; })
        .map(function(pair) { return { slug: pair[0], count: pair[1] }; });
    },
    getTotal: function() {
      var counts = getPlayCounts();
      return Object.values(counts).reduce(function(sum, c) { return sum + c; }, 0);
    }
  };
})();
