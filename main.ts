import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const outputDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const sourceFile = join(dirname(fileURLToPath(import.meta.url)), "entry.png");
const destinationFile = join(outputDir, "entry.png");

try {
  if (!existsSync(outputDir)) {
    mkdirSync(outputDir, { recursive: true });
  }
  copyFileSync(sourceFile, destinationFile);
} catch (error) {
  const reason = error instanceof Error ? error.message : String(error);
  throw new Error(
    `Unable to copy ${sourceFile} to ${destinationFile}: ${reason}`,
    { cause: error },
  );
}
