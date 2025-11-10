import { logger, task, schedules } from "@trigger.dev/sdk/v3";
import { execFile } from "node:child_process";
import { promises as fs } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);

const DEFAULT_TEXT = "TRIGGER";
const DEFAULT_REPO_PATH = path.resolve(process.cwd(), ".cache/github-contribution-art");

const bundledScriptPath = fileURLToPath(new URL("../python/github-contribution-art.py", import.meta.url));

async function resolveScriptPath(): Promise<string> {
  const candidates = [
    bundledScriptPath,
    path.resolve(process.cwd(), "src/python/github-contribution-art.py"),
    path.resolve(process.cwd(), "python/github-contribution-art.py"),
  ];

  for (const candidate of candidates) {
    try {
      const stats = await fs.stat(candidate);
      if (stats.isFile()) {
        return candidate;
      }
    } catch {
      // try next
    }
  }

  throw new Error("Unable to locate github-contribution-art.py in the deployed bundle.");
}

export const updateGithubContributions = task({
  id: "update-github-contributions",
  maxDuration: 300,
  run: async (payload: any) => {
    const text = payload?.text ?? process.env.GITHUB_CONTRIBUTION_TEXT ?? DEFAULT_TEXT;
    const repoPath =
      payload?.repoPath ?? process.env.GITHUB_CONTRIBUTION_REPO_PATH ?? DEFAULT_REPO_PATH;
    const remoteUrl =
      payload?.remoteUrl ?? process.env.GITHUB_CONTRIBUTION_REMOTE_URL ?? undefined;
    const branch = payload?.branch ?? process.env.GITHUB_CONTRIBUTION_BRANCH ?? "main";

    const scriptPath = await resolveScriptPath();

    logger.info("Regenerating GitHub contributions art", {
      text,
      repoPath,
      hasRemote: Boolean(remoteUrl),
      branch,
      scriptPath,
    });

    const args = [
      scriptPath,
      "--text",
      text,
      "--repo-path",
      repoPath,
      "--branch",
      branch,
      "--quiet",
      "--json",
      ...(remoteUrl ? ["--remote-url", remoteUrl] : []),
    ];

    try {
      const { stdout, stderr } = await execFileAsync("python3", args, {
        env: { ...process.env },
        maxBuffer: 10 * 1024 * 1024,
      });

      if (stderr.trim().length > 0) {
        logger.warn("GitHub contributions art generator warnings", { stderr });
      }

      let summary: Record<string, unknown> | undefined;
      const stdoutLines = stdout.split(/\r?\n/).filter(Boolean);
      if (stdoutLines.length > 0) {
        const lastLine = stdoutLines[stdoutLines.length - 1];
        try {
          summary = JSON.parse(lastLine);
        } catch {
          logger.warn("Unable to parse JSON summary from generator output", { lastLine });
        }
      }

      return {
        text,
        repoPath,
        remoteUrlConfigured: Boolean(remoteUrl),
        branch,
        summary,
      };
    } catch (error) {
      logger.error("Failed to regenerate GitHub contributions art", { error });
      throw error;
    }
  },
});

export const updateGithubContributionsDaily = schedules.task({
  id: "update-github-contributions-daily",
  cron: "0 6 * * *",
  run: async () => {
    return await updateGithubContributions.trigger({});
  },
});