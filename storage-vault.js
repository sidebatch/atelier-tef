/* TEF Atelier 저장 금고 (전 페이지 공용)
   목적: 브라우저가 localStorage를 정리해도 학습 기록이 살아남게 한다.
   1) navigator.storage.persist() — 브라우저 자동 회수에서 제외해 달라고 신청
   2) IndexedDB 이중 백업 — 저장할 때마다 금고에도 같은 내용을 넣어 둔다
   3) 자동 복원 — localStorage에서 사라진 키가 있으면 금고에서 되살린다
   IndexedDB가 없는 환경에서는 조용히 아무 일도 하지 않는다. */
(function () {
  if (window.Vault) return;
  var DB_NAME = "tef-atelier-vault", STORE = "kv", INDEX_KEY = "__vault_keys__";
  var hasIDB = typeof indexedDB !== "undefined";
  var memKeys = null, indexTimer = 0;

  function openDB() {
    return new Promise(function (res, rej) {
      if (!hasIDB) return rej(new Error("no indexedDB"));
      var rq = indexedDB.open(DB_NAME, 1);
      rq.onupgradeneeded = function () { rq.result.createObjectStore(STORE); };
      rq.onsuccess = function () { res(rq.result); };
      rq.onerror = function () { rej(rq.error); };
    });
  }
  function idbPut(key, val) {
    return openDB().then(function (db) {
      return new Promise(function (res, rej) {
        var tx = db.transaction(STORE, "readwrite");
        tx.objectStore(STORE).put(val, key);
        tx.oncomplete = function () { res(true); };
        tx.onerror = function () { rej(tx.error); };
      });
    }).catch(function () { return false; });
  }
  function idbGet(key) {
    return openDB().then(function (db) {
      return new Promise(function (res, rej) {
        var rq = db.transaction(STORE, "readonly").objectStore(STORE).get(key);
        rq.onsuccess = function () { res(rq.result); };
        rq.onerror = function () { rej(rq.error); };
      });
    }).catch(function () { return undefined; });
  }
  function idbDelete(key) {
    return openDB().then(function (db) {
      return new Promise(function (res) {
        var tx = db.transaction(STORE, "readwrite");
        tx.objectStore(STORE).delete(key);
        tx.oncomplete = function () { res(true); };
        tx.onerror = function () { res(false); };
      });
    }).catch(function () { return false; });
  }

  function persist() {
    try {
      if (navigator.storage && navigator.storage.persist) {
        var p = navigator.storage.persist();
        if (p && p.catch) p.catch(function () {});
      }
    } catch (e) {}
  }
  function persisted() {
    try {
      if (navigator.storage && navigator.storage.persisted) return navigator.storage.persisted();
    } catch (e) {}
    return Promise.resolve(false);
  }

  function flushIndex() {
    if (!memKeys || !hasIDB) return;
    idbGet(INDEX_KEY).then(function (prev) {
      var set = new Set(Array.isArray(prev) ? prev : []);
      memKeys.forEach(function (k) { set.add(k); });
      idbPut(INDEX_KEY, Array.from(set));
    });
  }
  function scheduleIndex() {
    if (indexTimer) return;
    indexTimer = setTimeout(function () { indexTimer = 0; flushIndex(); }, 3000);
  }
  function mirror(key, val) {
    if (!hasIDB || typeof key !== "string" || typeof val !== "string") return;
    idbPut(key, val);
    if (!memKeys) memKeys = new Set();
    if (!memKeys.has(key)) { memKeys.add(key); scheduleIndex(); }
  }
  function forget(key) {
    if (memKeys) memKeys.delete(key);
    if (!hasIDB) return;
    idbDelete(key);
    idbGet(INDEX_KEY).then(function (prev) {
      if (Array.isArray(prev)) idbPut(INDEX_KEY, prev.filter(function (k) { return k !== key; }));
    });
  }
  function restoreMissing() {
    if (!hasIDB) return Promise.resolve(0);
    return idbGet(INDEX_KEY).then(function (keys) {
      if (!Array.isArray(keys) || !keys.length) return 0;
      var missing = keys.filter(function (k) {
        try { return localStorage.getItem(k) === null; } catch (e) { return false; }
      });
      if (!missing.length) return 0;
      return Promise.all(missing.map(function (k) {
        return idbGet(k).then(function (v) {
          if (typeof v === "string") { try { localStorage.setItem(k, v); return 1; } catch (e) {} }
          return 0;
        });
      })).then(function (rs) { return rs.reduce(function (a, b) { return a + b; }, 0); });
    });
  }
  window.addEventListener("pagehide", function () {
    if (indexTimer) { clearTimeout(indexTimer); indexTimer = 0; }
    flushIndex();
  });

  function peek(key) { return idbGet(key); }
  window.Vault = { mirror: mirror, forget: forget, restoreMissing: restoreMissing, peek: peek, persist: persist, persisted: persisted };
})();
