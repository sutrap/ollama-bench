const { spawnSync } = require("child_process");
const path = require("path");

const root = path.join(__dirname, "..");
const script = path.join(root, "generate_promptfoo_config.py");
const candidates =
  process.platform === "win32"
    ? ["py", "python", "python3"]
    : ["python3", "python"];

for (const launcher of candidates) {
  const result = spawnSync(launcher, [script, ...process.argv.slice(2)], {
    cwd: root,
    stdio: "inherit",
  });
  if (result.error) {
    continue;
  }
  process.exit(result.status === null ? 1 : result.status);
}

console.error(
  "Python konnte nicht gefunden werden. Bitte installiere Python und stelle sicher, dass es im PATH ist."
);
process.exit(1);