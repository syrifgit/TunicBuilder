/*
 * Smoke test for a built page: does its script actually run?
 *
 *   node check.js tunic.html
 *
 * `node --check` only parses. It will happily pass a file that throws
 * ReferenceError the moment it runs - which is exactly what happens when a
 * refactor drops a function that something else still calls. This executes the
 * page against a stub DOM, so a missing identifier or a null property surfaces
 * here instead of as a blank drawing in the browser.
 *
 * The stub is deliberately dumb: it does not verify anything about the output,
 * only that the code completes a full render without throwing.
 */
const fs = require("fs");
const vm = require("vm");
const path = require("path");

function stubElement(tag) {
  const el = {
    tagName: tag,
    children: [],
    style: {},
    dataset: {},
    _attrs: {},
    textContent: "",
    innerHTML: "",
    value: "",
    checked: false,
    type: "",
    classList: { toggle() {}, add() {}, remove() {}, contains: () => false },
    setAttribute(k, v) { this._attrs[k] = v; },
    getAttribute(k) { return this._attrs[k]; },
    appendChild(c) { this.children.push(c); return c; },
    addEventListener() {},
    removeEventListener() {},
    querySelector() { return stubElement("div"); },
    querySelectorAll() { return []; },
    remove() {},
    focus() {},
  };
  return el;
}

function run(file) {
  const html = fs.readFileSync(file, "utf8");
  const blocks = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map((m) => m[1]);
  if (!blocks.length) {
    console.error(`${file}: no <script> blocks found`);
    return 1;
  }

  const asked = new Set();
  const document = {
    getElementById(id) { asked.add(id); return stubElement("div"); },
    createElement: stubElement,
    createElementNS: (_ns, t) => stubElement(t),
    body: stubElement("body"),
    documentElement: stubElement("html"),
    activeElement: null,
    addEventListener() {},
    querySelector: () => stubElement("div"),
    querySelectorAll: () => [],
  };

  // The stub only needs to be complete enough not to raise errors a real browser
  // would not. A gap here shows up as a false failure, which is worse than no check.
  const win = {
    claude: undefined,
    addEventListener() {}, removeEventListener() {},
    innerWidth: 1280, innerHeight: 900, devicePixelRatio: 1,
    matchMedia: () => ({ matches: false, addEventListener() {}, addListener() {} }),
    getComputedStyle: () => ({ getPropertyValue: () => "" }),
    requestAnimationFrame: (fn) => setTimeout(fn, 0),
    setTimeout, clearTimeout,
  };

  const ctx = {
    document,
    window: win,
    localStorage: { getItem: () => null, setItem() {}, removeItem() {} },
    console, setTimeout, clearTimeout,
    Math, JSON, Object, Array, String, Number, Date, Boolean, Error,
    parseFloat, parseInt, isNaN, encodeURIComponent, decodeURIComponent,
  };
  ctx.globalThis = ctx;

  try {
    // one context, because the browser shares scope across script blocks
    vm.runInNewContext(blocks.join("\n"), ctx, { filename: path.basename(file) });
  } catch (e) {
    console.error(`${file}: FAILED at runtime`);
    console.error(`  ${e.constructor.name}: ${e.message}`);
    const frame = (e.stack || "").split("\n").find((l) => l.includes(path.basename(file)));
    if (frame) console.error(`  ${frame.trim()}`);
    return 1;
  }

  console.log(`${file}: ran clean (${blocks.length} script blocks, ` +
              `${asked.size} elements requested)`);
  return 0;
}

const files = process.argv.slice(2);
if (!files.length) {
  console.error("usage: node check.js <built.html> [...]");
  process.exit(2);
}
process.exit(files.map(run).reduce((a, b) => a || b, 0));
