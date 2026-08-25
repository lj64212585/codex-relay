"use strict";

const translations = {
  "zh-CN": {
    "app.title": "Relay Installer",
    "meta.description": "为当前用户或指定项目安装 Codex Relay 调度包。",
    skip: "跳到安装设置",
    "brand.home": "Relay Installer 首页",
    "brand.subtitle": "Local setup console",
    localOnly: "仅在本机运行",
    "language.group": "语言选择",
    "language.toChinese": "切换到中文",
    "language.toEnglish": "Switch to English",
    "theme.label": "夜间模式",
    "theme.enable": "开启夜间模式",
    "theme.disable": "关闭夜间模式",
    "hero.title": "安装你的 Relay 调度",
    "hero.copy": "选择范围与类型，安装器会先检查冲突，再执行可恢复的安全切换。",
    "flow.label": "安装流程",
    "flow.scope": "选择范围",
    "flow.conflict": "检查冲突",
    "flow.install": "安装校验",
    "form.eyebrow": "Installation",
    "form.title": "配置安装",
    "form.count": "3 个步骤",
    "scope.title": "安装范围",
    "scope.help": "全局仅作用于当前用户；项目安装只在指定仓库生效。",
    "scope.global": "全局",
    "scope.globalHelp": "当前用户的所有项目可发现",
    "scope.project": "项目",
    "scope.projectHelp": "只在指定项目内生效",
    "scope.note": "只写入配置声明的 Skill 和 Agent 文件，不修改父目录中的其他内容。",
    "scope.removeButton": "移除当前目录的调度文件",
    "destination.globalLabel": "当前用户安装目录",
    "destination.loading": "正在读取…",
    "destination.projectLabel": "项目安装目录",
    "destination.placeholder": "例如 D:\\Projects\\my-project",
    "destination.browse": "浏览目录",
    "destination.help": "写入 .agents/skills 与 .codex/agents。",
    "destination.required": "请选择或输入一个项目安装目录。",
    "relay.title": "Relay 类型",
    "relay.help": "同一安装范围建议只保留一种主调度策略。",
    "relay.agentCount": "{count} 个 Agent",
    "relay.taskPerfection": "任务实现完美度",
    "relay.implementationCost": "实现成本",
    "relay.metricsHint": "相对单个 Sol 独立完成（100%）的估值；并非实测 benchmark。",
    "relay.metricsAria": "任务实现完美度 {quality}%，实现成本 {cost}%。相对单个 Sol 独立完成（100%）的估值。",
    "relay.details": "详情",
    "relay.detailsAria": "查看 {name} 的 README",
    "readme.eyebrow": "Relay 文档",
    "readme.close": "关闭",
    "readme.closeAria": "关闭 README 面板",
    "readme.languageZh": "中文 README",
    "readme.languageEn": "English README",
    "readme.loadingTitle": "正在读取 README",
    "readme.loadingCopy": "从当前 Relay 包载入对应语言的本地文档。",
    "readme.errorTitle": "README 载入失败",
    "readme.errorCopy": "无法读取当前语言的 README，请检查配置文件和终端日志。",
    "readme.unavailableTitle": "当前语言暂无 README",
    "readme.unavailableCopy": "请在配置文件中为此 Relay 声明对应语言的 README。",
    "install.title": "检查并安装",
    "install.help": "先只读检查；确认冲突处理后才会改动文件。",
    "install.button": "检查并安装",
    "install.checking": "正在检查",
    "install.installing": "正在安装",
    "install.waiting": "等待目录选择",
    "install.unavailable": "无法启动",
    "summary.title": "安装摘要",
    "summary.loading": "准备中",
    "summary.scope": "安装范围",
    "summary.path": "目标根目录",
    "summary.content": "写入内容",
    "summary.global": "全局 · 当前用户",
    "summary.project": "项目",
    "summary.pathPending": "尚未选择项目目录",
    "summary.relayPending": "尚未选择",
    "summary.contentPending": "Skill + Agent profiles",
    "summary.contentValue": "1 个 Skill + {count} 个 Agent profiles",
    "summary.localNote": "服务仅监听 127.0.0.1；关闭终端即可停止。",
    "summary.pending": "待检查",
    "summary.ready": "可安装",
    "summary.warning": "有冲突",
    "summary.blocked": "已阻止",
    "summary.unavailable": "不可用",
    "preflight.pendingTitle": "冲突检查尚未运行",
    "preflight.pendingCopy": "安装前将检查此位置的已知 Relay 与同名文件。",
    "preflight.unmanagedTitle": "发现无法确认归属的同名内容",
    "preflight.unmanagedCopy": "为避免覆盖自定义文件，安装器已停止。请先手动核对目标路径。",
    "preflight.conflictTitle": "发现 {count} 种其他调度",
    "preflight.conflictCopy": "需要确认移除其他调度后才能继续安装。",
    "preflight.currentTitle": "当前 Relay 已存在，可安全更新",
    "preflight.currentCopy": "现有同类型内容会先备份，再由配置中的源文件替换。",
    "preflight.readyTitle": "未发现其他 Relay 冲突",
    "preflight.readyCopy": "目标位置可以安装当前选择的 Relay。",
    "config.before": "Relay 源目录来自",
    "config.button": "配置文件",
    "config.hide": "隐藏配置路径",
    "config.after": "，网页不写死包路径。",
    "dialog.eyebrow": "检测到其他调度",
    "dialog.title": "多个 Relay 会产生调度冲突",
    "dialog.warning": "多个调度 Skill 会竞争同一任务；如果共享 Agent 名称，配置还会互相覆盖，导致实际执行角色与预期不一致。",
    "dialog.backup": "继续后，其他 Relay 会先从活动位置移除并保存可恢复备份，再安装当前选择。",
    "dialog.cancel": "取消",
    "dialog.confirm": "移除其他调度并安装",
    "dialog.installed": "完整安装",
    "dialog.partial": "部分残留",
    "remove.inspecting": "正在检查可移除内容",
    "remove.removing": "正在移除调度",
    "removeDialog.eyebrow": "移除调度文件",
    "removeDialog.title": "确认移除当前目录的调度？",
    "removeDialog.warning": "下列 Relay 的 Skill 与 Agent 文件会从活动目录移出；目录中的其他文件不会被修改。",
    "removeDialog.target": "目标目录",
    "removeDialog.backup": "确认后，识别到的调度文件会先保存到可恢复备份，再从当前目录移除。",
    "removeDialog.cancel": "取消",
    "removeDialog.confirm": "移除并备份",
    "result.successTitle": "安装完成",
    "result.installSuccess": "{relay} 已安装完成。",
    "result.removeSuccessTitle": "调度已移除",
    "result.removeSuccess": "已从当前目录移除 {count} 种已识别 Relay。",
    "result.removeEmptyTitle": "没有可移除的调度",
    "result.removeEmptyCopy": "目标目录中未发现由此安装器识别的 Relay 文件。",
    "result.removeFailTitle": "移除失败",
    "result.location": "安装位置",
    "result.removed": "已移除",
    "result.backup": "备份",
    "result.paths": "相关路径",
    "result.blockedTitle": "安装已阻止",
    "result.blockedCopy": "目标位置存在无法确认归属的同名内容，请先手动核对。",
    "result.installFailTitle": "安装失败",
    "result.checkFailTitle": "检查失败",
    "result.browseFailTitle": "无法浏览目录",
    "result.initFailTitle": "初始化失败",
    "result.initFailCopy": "无法读取安装器配置。",
    "result.initialCheckTitle": "初始检查失败",
    "result.initialCheckHint": "仍可切换安装范围或选择其他项目目录后重试。",
    "errors.validation_error": "安装范围或目标目录无效，请检查输入后重试。",
    "errors.relay_conflict": "检测到其他 Relay 调度，确认移除后才能继续。",
    "errors.unmanaged_collision": "目标位置存在无法确认归属的同名内容。",
    "errors.installer_error": "安装操作未能完成，请稍后重试。",
    "errors.config_error": "安装器配置无效。",
    "errors.invalid_session": "安装器会话已失效，请刷新页面。",
    "errors.internal_error": "安装器发生未预期错误，请查看终端日志。",
    "errors.default": "请求失败，请检查终端日志后重试。"
  },
  en: {
    "app.title": "Relay Installer",
    "meta.description": "Install a Codex Relay for the current user or a selected project.",
    skip: "Skip to installer settings",
    "brand.home": "Relay Installer home",
    "brand.subtitle": "Local setup console",
    localOnly: "Local only",
    "language.group": "Language",
    "language.toChinese": "Switch to Chinese",
    "language.toEnglish": "Switch to English",
    "theme.label": "Dark mode",
    "theme.enable": "Enable dark mode",
    "theme.disable": "Disable dark mode",
    "hero.title": "Install your Relay workflow",
    "hero.copy": "Choose a scope and Relay. The installer checks conflicts before making a recoverable switch.",
    "flow.label": "Installation flow",
    "flow.scope": "Choose scope",
    "flow.conflict": "Check conflicts",
    "flow.install": "Verify install",
    "form.eyebrow": "Installation",
    "form.title": "Configure install",
    "form.count": "3 steps",
    "scope.title": "Install scope",
    "scope.help": "Global applies to the current user; project scope stays inside one repository.",
    "scope.global": "Global",
    "scope.globalHelp": "Discoverable from every project",
    "scope.project": "Project",
    "scope.projectHelp": "Active only in the selected project",
    "scope.note": "Only the Skill and Agent files declared in config are written. Other parent-directory content is preserved.",
    "scope.removeButton": "Remove Relay files from this directory",
    "destination.globalLabel": "Current user install directory",
    "destination.loading": "Loading…",
    "destination.projectLabel": "Project install directory",
    "destination.placeholder": "e.g. D:\\Projects\\my-project",
    "destination.browse": "Browse",
    "destination.help": "Writes to .agents/skills and .codex/agents.",
    "destination.required": "Select or enter a project install directory.",
    "relay.title": "Relay type",
    "relay.help": "Keep one primary orchestration strategy in each install scope.",
    "relay.agentCount": "{count} Agents",
    "relay.taskPerfection": "Task perfection",
    "relay.implementationCost": "Implementation cost",
    "relay.metricsHint": "Estimated relative to one Sol working independently (100%); not a measured benchmark.",
    "relay.metricsAria": "Task perfection {quality}%, implementation cost {cost}%. Estimated relative to one Sol working independently (100%).",
    "relay.details": "Details",
    "relay.detailsAria": "View the {name} README",
    "readme.eyebrow": "Relay documentation",
    "readme.close": "Close",
    "readme.closeAria": "Close README panel",
    "readme.languageZh": "Chinese README",
    "readme.languageEn": "English README",
    "readme.loadingTitle": "Loading README",
    "readme.loadingCopy": "Reading the matching local document from this Relay package.",
    "readme.errorTitle": "Could not load README",
    "readme.errorCopy": "The README for this language could not be read. Check the config and terminal log.",
    "readme.unavailableTitle": "No README for this language",
    "readme.unavailableCopy": "Declare a matching README for this Relay in the installer config.",
    "install.title": "Check and install",
    "install.help": "Preflight is read-only. Files change only after conflict confirmation.",
    "install.button": "Check and install",
    "install.checking": "Checking",
    "install.installing": "Installing",
    "install.waiting": "Waiting for folder",
    "install.unavailable": "Unavailable",
    "summary.title": "Install summary",
    "summary.loading": "Preparing",
    "summary.scope": "Install scope",
    "summary.path": "Target root",
    "summary.content": "Writes",
    "summary.global": "Global · Current user",
    "summary.project": "Project",
    "summary.pathPending": "No project directory selected",
    "summary.relayPending": "Not selected",
    "summary.contentPending": "Skill + Agent profiles",
    "summary.contentValue": "1 Skill + {count} Agent profiles",
    "summary.localNote": "The service listens only on 127.0.0.1. Close the terminal to stop it.",
    "summary.pending": "Pending",
    "summary.ready": "Ready",
    "summary.warning": "Conflict",
    "summary.blocked": "Blocked",
    "summary.unavailable": "Unavailable",
    "preflight.pendingTitle": "Conflict check has not run",
    "preflight.pendingCopy": "Known Relays and same-name files are checked before installation.",
    "preflight.unmanagedTitle": "Unmanaged same-name content found",
    "preflight.unmanagedCopy": "The installer stopped to protect custom files. Review the target paths manually.",
    "preflight.conflictTitle": "Detected {count} other Relay installation(s)",
    "preflight.conflictCopy": "Confirm removal of the other Relay before continuing.",
    "preflight.currentTitle": "This Relay is installed and can be updated",
    "preflight.currentCopy": "The current copy is backed up before replacement from the configured source.",
    "preflight.readyTitle": "No other Relay conflicts found",
    "preflight.readyCopy": "The selected Relay can be installed at this target.",
    "config.before": "Relay sources come from the",
    "config.button": "config file",
    "config.hide": "hide config path",
    "config.after": "; package paths are not hard-coded in the page.",
    "dialog.eyebrow": "Other orchestration detected",
    "dialog.title": "Multiple Relays create routing conflicts",
    "dialog.warning": "Multiple orchestration Skills can compete for the same task. Shared Agent names can also overwrite profiles and change which role actually runs.",
    "dialog.backup": "Continuing removes the other Relay from the active target, saves a recoverable backup, and then installs your selection.",
    "dialog.cancel": "Cancel",
    "dialog.confirm": "Remove other Relay and install",
    "dialog.installed": "Installed",
    "dialog.partial": "Partial remains",
    "remove.inspecting": "Checking removable files",
    "remove.removing": "Removing Relay files",
    "removeDialog.eyebrow": "Remove Relay files",
    "removeDialog.title": "Remove orchestration from this directory?",
    "removeDialog.warning": "The Skill and Agent files for the Relays below will leave the active directory. Other files in the directory are preserved.",
    "removeDialog.target": "Target directory",
    "removeDialog.backup": "The recognized Relay files are saved to a recoverable backup before they are removed from this directory.",
    "removeDialog.cancel": "Cancel",
    "removeDialog.confirm": "Remove and back up",
    "result.successTitle": "Installation complete",
    "result.installSuccess": "{relay} was installed successfully.",
    "result.removeSuccessTitle": "Orchestration removed",
    "result.removeSuccess": "Recognized Relay installations removed from this directory: {count}.",
    "result.removeEmptyTitle": "No Relay files to remove",
    "result.removeEmptyCopy": "No Relay files recognized by this installer were found in the target directory.",
    "result.removeFailTitle": "Removal failed",
    "result.location": "Location",
    "result.removed": "Removed",
    "result.backup": "Backup",
    "result.paths": "Related paths",
    "result.blockedTitle": "Installation blocked",
    "result.blockedCopy": "The target contains same-name content whose ownership cannot be confirmed. Review it manually.",
    "result.installFailTitle": "Installation failed",
    "result.checkFailTitle": "Preflight failed",
    "result.browseFailTitle": "Could not browse folders",
    "result.initFailTitle": "Initialization failed",
    "result.initFailCopy": "The installer configuration could not be loaded.",
    "result.initialCheckTitle": "Initial preflight failed",
    "result.initialCheckHint": "You can still change scope or select another project directory and try again.",
    "errors.validation_error": "The install scope or target directory is invalid. Check the input and try again.",
    "errors.relay_conflict": "Another Relay is installed. Confirm its removal before continuing.",
    "errors.unmanaged_collision": "The target contains same-name content with unknown ownership.",
    "errors.installer_error": "The installation could not be completed. Try again.",
    "errors.config_error": "The installer configuration is invalid.",
    "errors.invalid_session": "The installer session expired. Refresh the page.",
    "errors.internal_error": "The installer hit an unexpected error. Check the terminal log.",
    "errors.default": "The request failed. Check the terminal log and try again."
  }
};

const state = {
  bootstrap: null,
  sessionToken: "",
  locale: "zh-CN",
  scope: "global",
  projectPath: "",
  relayId: "",
  busy: false,
  busyLabelKey: "install.button",
  busyAction: "",
  inspection: null,
  removalInspection: null,
  result: null,
  readmeRelayId: "",
  readmeRequestKey: "",
  readmeCache: new Map()
};

const elements = {
  form: document.getElementById("installer-form"),
  themeToggle: document.getElementById("theme-toggle"),
  languageOptions: Array.from(document.querySelectorAll(".language-option")),
  globalTargetField: document.getElementById("global-target-field"),
  globalTargetPath: document.getElementById("global-target-path"),
  projectPathField: document.getElementById("project-path-field"),
  projectPathInput: document.getElementById("project-path"),
  projectPathError: document.getElementById("project-path-error"),
  browseButton: document.getElementById("browse-button"),
  removeRelaysButton: document.getElementById("remove-relays-button"),
  removeRelaysButtonLabel: document.querySelector(
    "#remove-relays-button .remove-button-label"
  ),
  relayOptions: document.getElementById("relay-options"),
  installButton: document.getElementById("install-button"),
  installButtonLabel: document.querySelector("#install-button .button-label"),
  resultPanel: document.getElementById("result-panel"),
  resultTitle: document.getElementById("result-title"),
  resultMessage: document.getElementById("result-message"),
  resultDetails: document.getElementById("result-details"),
  summaryScope: document.getElementById("summary-scope"),
  summaryPath: document.getElementById("summary-path"),
  summaryRelay: document.getElementById("summary-relay"),
  summaryContent: document.getElementById("summary-content"),
  summaryState: document.getElementById("summary-state"),
  summaryStateLabel: document.querySelector("#summary-state .summary-state-label"),
  preflightMessage: document.getElementById("preflight-message"),
  configPathButton: document.getElementById("config-path-button"),
  configPath: document.getElementById("config-path"),
  conflictDialog: document.getElementById("conflict-dialog"),
  conflictList: document.getElementById("conflict-list"),
  cancelConflictButton: document.getElementById("cancel-conflict-button"),
  confirmConflictButton: document.getElementById("confirm-conflict-button"),
  removeDialog: document.getElementById("remove-dialog"),
  removeRelayList: document.getElementById("remove-relay-list"),
  removeTargetPath: document.getElementById("remove-target-path"),
  cancelRemoveButton: document.getElementById("cancel-remove-button"),
  confirmRemoveButton: document.getElementById("confirm-remove-button"),
  readmeDialog: document.getElementById("readme-dialog"),
  readmeTitle: document.getElementById("readme-title"),
  readmeLanguage: document.getElementById("readme-language"),
  readmeFileName: document.getElementById("readme-file-name"),
  readmeStatus: document.getElementById("readme-status"),
  readmeContent: document.getElementById("readme-content"),
  readmeCloseButton: document.getElementById("readme-close-button")
};

class ApiError extends Error {
  constructor(error, status) {
    super(error && error.message ? error.message : "Request failed.");
    this.name = "ApiError";
    this.code = error && error.code ? error.code : "unknown_error";
    this.details = error ? error.details : null;
    this.status = status;
  }
}

function t(key, parameters) {
  const localeTable = translations[state.locale] || translations["zh-CN"];
  let value = localeTable[key];
  if (typeof value !== "string") {
    value = translations["zh-CN"][key] || key;
  }
  return value.replace(/\{(\w+)\}/g, function (_match, name) {
    return parameters && parameters[name] !== undefined
      ? String(parameters[name])
      : "{" + name + "}";
  });
}

function translatedError(error) {
  if (error instanceof ApiError) {
    const key = "errors." + error.code;
    if (Object.prototype.hasOwnProperty.call(translations[state.locale], key)) {
      return t(key);
    }
    if (state.locale === "zh-CN" && error.message) {
      return error.message;
    }
  }
  return t("errors.default");
}

function localizedRelay(relay) {
  if (!relay) {
    return null;
  }
  const localized =
    state.locale !== "zh-CN" &&
    relay.translations &&
    relay.translations[state.locale]
      ? relay.translations[state.locale]
      : null;
  return {
    id: relay.id,
    name: localized ? localized.name : relay.name,
    badge: localized ? localized.badge : relay.badge,
    description: localized ? localized.description : relay.description,
    metrics: relay.metrics,
    agentCount: relay.agentCount,
    targets: relay.targets,
    readmeLocales: Array.isArray(relay.readmeLocales)
      ? relay.readmeLocales
      : []
  };
}

function relayNameById(relayId, fallbackName) {
  if (!state.bootstrap) {
    return fallbackName || relayId;
  }
  const relay = state.bootstrap.relays.find(function (item) {
    return item.id === relayId;
  });
  const localized = localizedRelay(relay);
  return localized ? localized.name : fallbackName || relayId;
}

function getSelectedRelay() {
  if (!state.bootstrap) {
    return null;
  }
  const relay = state.bootstrap.relays.find(function (item) {
    return item.id === state.relayId;
  });
  return localizedRelay(relay);
}

function applyLanguage(locale, persist) {
  state.locale = locale === "en" ? "en" : "zh-CN";
  document.documentElement.lang = state.locale;
  document.title = t("app.title");

  document.querySelectorAll("[data-i18n]").forEach(function (element) {
    element.textContent = t(element.dataset.i18n);
  });
  document
    .querySelectorAll("[data-i18n-aria-label]")
    .forEach(function (element) {
      element.setAttribute("aria-label", t(element.dataset.i18nAriaLabel));
    });
  document
    .querySelectorAll("[data-i18n-placeholder]")
    .forEach(function (element) {
      element.setAttribute("placeholder", t(element.dataset.i18nPlaceholder));
    });
  document
    .querySelectorAll("[data-i18n-content]")
    .forEach(function (element) {
      element.setAttribute("content", t(element.dataset.i18nContent));
    });

  elements.languageOptions.forEach(function (button) {
    const active = button.dataset.locale === state.locale;
    button.classList.toggle("is-active", active);
    button.setAttribute("aria-pressed", String(active));
  });
  if (persist !== false) {
    localStorage.setItem("relay-installer-locale", state.locale);
  }

  updateThemeA11y();
  updateConfigPathButton();
  if (elements.projectPathInput.getAttribute("aria-invalid") === "true") {
    elements.projectPathError.textContent = t("destination.required");
  }
  if (state.bootstrap) {
    renderRelays(state.bootstrap.relays);
    updateSummary();
    updatePreflight(state.inspection);
  }
  renderResult();
  if (elements.conflictDialog.open && state.inspection) {
    renderConflictList(state.inspection);
  }
  if (elements.readmeDialog.open && state.readmeRelayId) {
    openReadme(state.readmeRelayId, false);
  }
  if (elements.removeDialog.open && state.removalInspection) {
    renderRelayDetectionList(
      elements.removeRelayList,
      state.removalInspection.installations
    );
  }
  setBusy(state.busy, state.busyLabelKey, state.busyAction);
}

function initializeLanguage() {
  const stored = localStorage.getItem("relay-installer-locale");
  const preferred = navigator.language.toLowerCase().startsWith("zh")
    ? "zh-CN"
    : "en";
  applyLanguage(stored || preferred, false);
}

function updateThemeA11y() {
  const isDark = document.documentElement.dataset.theme === "dark";
  elements.themeToggle.setAttribute("aria-checked", String(isDark));
  elements.themeToggle.setAttribute(
    "aria-label",
    t(isDark ? "theme.disable" : "theme.enable")
  );
}

function setTheme(theme) {
  document.documentElement.dataset.theme = theme;
  localStorage.setItem("relay-installer-theme", theme);
  updateThemeA11y();
}

function initializeTheme() {
  const stored = localStorage.getItem("relay-installer-theme");
  const preferredDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  setTheme(stored || (preferredDark ? "dark" : "light"));
}

async function apiRequest(path, payload) {
  const response = await fetch(path, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Installer-Token": state.sessionToken
    },
    body: JSON.stringify(payload || {})
  });
  const data = await response.json();
  if (!response.ok || !data.ok) {
    throw new ApiError(data.error, response.status);
  }
  return data.data;
}

function targetPayload() {
  return {
    scope: state.scope,
    projectPath:
      state.scope === "project" ? elements.projectPathInput.value.trim() : null,
    locale: state.locale
  };
}

function installPayload(removeConflicts) {
  return {
    ...targetPayload(),
    relayId: state.relayId,
    removeConflicts: removeConflicts === true
  };
}

function setBusy(isBusy, labelKey, action) {
  state.busy = isBusy;
  state.busyLabelKey = labelKey || "install.button";
  state.busyAction = isBusy ? action || "install" : "";
  elements.installButton.disabled = isBusy || !state.bootstrap;
  elements.installButton.classList.toggle(
    "is-busy",
    isBusy && state.busyAction === "install"
  );
  elements.installButtonLabel.textContent = t(
    isBusy && state.busyAction === "install"
      ? state.busyLabelKey
      : "install.button"
  );
  elements.removeRelaysButton.disabled = isBusy || !state.bootstrap;
  elements.removeRelaysButton.classList.toggle(
    "is-busy",
    isBusy && state.busyAction === "remove"
  );
  elements.removeRelaysButtonLabel.textContent = t(
    isBusy && state.busyAction === "remove"
      ? state.busyLabelKey
      : "scope.removeButton"
  );
  elements.browseButton.disabled = isBusy;
  elements.confirmConflictButton.disabled = isBusy;
  elements.confirmRemoveButton.disabled = isBusy;
}

function clearPathError() {
  elements.projectPathError.textContent = "";
  elements.projectPathInput.removeAttribute("aria-invalid");
}

function validateProjectPath() {
  clearPathError();
  if (
    state.scope === "project" &&
    elements.projectPathInput.value.trim().length === 0
  ) {
    elements.projectPathError.textContent = t("destination.required");
    elements.projectPathInput.setAttribute("aria-invalid", "true");
    elements.projectPathInput.focus();
    return false;
  }
  return true;
}

function setResult(result) {
  state.result = result;
  renderResult();
}

function clearResult() {
  state.result = null;
  renderResult();
}

function renderResult() {
  if (!state.result) {
    elements.resultPanel.hidden = true;
    elements.resultPanel.removeAttribute("data-status");
    elements.resultTitle.textContent = "";
    elements.resultMessage.textContent = "";
    elements.resultDetails.textContent = "";
    return;
  }

  const result = state.result;
  elements.resultPanel.hidden = false;
  elements.resultPanel.dataset.status = result.status;
  elements.resultPanel.setAttribute(
    "role",
    result.status === "error" ? "alert" : "status"
  );

  if (result.kind === "installSuccess") {
    const relayName = relayNameById(result.data.relay.id, result.data.relay.name);
    const removedNames = result.data.removedRelays.map(function (relay) {
      return relayNameById(relay.id, relay.name);
    });
    const details = [t("result.location") + ": " + result.data.targetRoot];
    if (removedNames.length > 0) {
      details.push(t("result.removed") + ": " + removedNames.join(", "));
    }
    if (result.data.backupPath) {
      details.push(t("result.backup") + ": " + result.data.backupPath);
    }
    elements.resultTitle.textContent = t("result.successTitle");
    elements.resultMessage.textContent = t("result.installSuccess", {
      relay: relayName
    });
    elements.resultDetails.textContent = details.join(" · ");
    return;
  }

  if (result.kind === "removeSuccess") {
    const removedNames = result.data.removedRelays.map(function (relay) {
      return relayNameById(relay.id, relay.name);
    });
    const details = [t("result.location") + ": " + result.data.targetRoot];
    if (removedNames.length > 0) {
      details.push(t("result.removed") + ": " + removedNames.join(", "));
    }
    if (result.data.backupPath) {
      details.push(t("result.backup") + ": " + result.data.backupPath);
    }
    elements.resultTitle.textContent = t("result.removeSuccessTitle");
    elements.resultMessage.textContent = t("result.removeSuccess", {
      count: result.data.removedRelays.length
    });
    elements.resultDetails.textContent = details.join(" · ");
    return;
  }

  elements.resultTitle.textContent = t(result.titleKey);
  elements.resultMessage.textContent = result.messageKey
    ? t(result.messageKey)
    : translatedError(result.error);
  elements.resultDetails.textContent = result.details || "";
}

function setSummaryState(status, labelKey, parameters) {
  elements.summaryState.dataset.status = status;
  elements.summaryStateLabel.textContent = t(labelKey, parameters);
}

function updateSummary() {
  if (!state.bootstrap) {
    return;
  }
  const relay = getSelectedRelay();
  elements.globalTargetPath.textContent = state.bootstrap.globalPath;
  elements.summaryScope.textContent = t(
    state.scope === "global" ? "summary.global" : "summary.project"
  );
  elements.summaryPath.textContent =
    state.scope === "global"
      ? state.bootstrap.globalPath
      : elements.projectPathInput.value.trim() || t("summary.pathPending");
  elements.summaryRelay.textContent = relay
    ? relay.name
    : t("summary.relayPending");
  elements.summaryContent.textContent = relay
    ? t("summary.contentValue", { count: relay.agentCount })
    : t("summary.contentPending");
}

function updatePreflight(inspection) {
  state.inspection = inspection;
  const title = elements.preflightMessage.querySelector("strong");
  const copy = elements.preflightMessage.querySelector("p");

  if (!inspection) {
    elements.preflightMessage.removeAttribute("data-status");
    title.textContent = t("preflight.pendingTitle");
    copy.textContent = t("preflight.pendingCopy");
    setSummaryState("", "summary.pending");
    return;
  }

  if (inspection.unmanagedCollisions.length > 0) {
    elements.preflightMessage.dataset.status = "error";
    title.textContent = t("preflight.unmanagedTitle");
    copy.textContent = t("preflight.unmanagedCopy");
    setSummaryState("warning", "summary.blocked");
    return;
  }

  if (inspection.conflicts.length > 0) {
    elements.preflightMessage.dataset.status = "warning";
    title.textContent = t("preflight.conflictTitle", {
      count: inspection.conflicts.length
    });
    copy.textContent = t("preflight.conflictCopy");
    setSummaryState("warning", "summary.warning");
    return;
  }

  elements.preflightMessage.dataset.status = "ready";
  title.textContent = t(
    inspection.currentInstallation
      ? "preflight.currentTitle"
      : "preflight.readyTitle"
  );
  copy.textContent = t(
    inspection.currentInstallation
      ? "preflight.currentCopy"
      : "preflight.readyCopy"
  );
  setSummaryState("ready", "summary.ready");
}

function createRelayOption(relay, checked) {
  const localized = localizedRelay(relay);
  const option = document.createElement("div");
  option.className = "relay-option";

  const detailsButton = document.createElement("button");
  detailsButton.type = "button";
  detailsButton.className = "relay-details-button";
  detailsButton.disabled = !localized.readmeLocales.includes(state.locale);
  detailsButton.setAttribute(
    "aria-label",
    t("relay.detailsAria", { name: localized.name })
  );
  detailsButton.title = detailsButton.getAttribute("aria-label");
  detailsButton.innerHTML =
    '<svg viewBox="0 0 24 24" aria-hidden="true">' +
    '<path d="M5 4.5h10.5A2.5 2.5 0 0 1 18 7v12.5H7.5A2.5 2.5 0 0 1 5 17Z"></path>' +
    '<path d="M5 17a2.5 2.5 0 0 1 2.5-2.5H18M9 8h5"></path>' +
    "</svg>" +
    '<span class="relay-details-label">' + t("relay.details") + "</span>";
  detailsButton.addEventListener("click", function () {
    openReadme(relay.id, true);
  });

  const label = document.createElement("label");
  label.className = "relay-choice";

  const input = document.createElement("input");
  input.type = "radio";
  input.name = "relay";
  input.value = relay.id;
  input.id = "relay-option-" + relay.id;
  input.checked = checked;
  input.addEventListener("change", function () {
    if (!input.checked) {
      return;
    }
    state.relayId = relay.id;
    clearResult();
    updateSummary();
    updatePreflight(null);
  });

  const top = document.createElement("span");
  top.className = "relay-option-top";
  const heading = document.createElement("h3");
  heading.textContent = localized.name;
  const check = document.createElement("span");
  check.className = "relay-check";
  check.setAttribute("aria-hidden", "true");
  check.innerHTML =
    '<svg viewBox="0 0 24 24"><path d="m6 12 4 4 8-8"></path></svg>';
  top.append(heading, check);

  const metrics = document.createElement("span");
  metrics.className = "relay-metrics";
  metrics.setAttribute("role", "group");
  metrics.title = t("relay.metricsHint");
  metrics.setAttribute(
    "aria-label",
    t("relay.metricsAria", {
      quality: localized.metrics.taskPerfectionPercent,
      cost: localized.metrics.implementationCostPercent
    })
  );

  [
    {
      kind: "quality",
      label: t("relay.taskPerfection"),
      value: localized.metrics.taskPerfectionPercent
    },
    {
      kind: "cost",
      label: t("relay.implementationCost"),
      value: localized.metrics.implementationCostPercent
    }
  ].forEach(function (metricDefinition) {
    const metric = document.createElement("span");
    metric.className = "relay-metric";
    metric.dataset.kind = metricDefinition.kind;

    const metricLabel = document.createElement("span");
    metricLabel.className = "relay-metric-label";
    metricLabel.textContent = metricDefinition.label;

    const metricValue = document.createElement("strong");
    metricValue.textContent = metricDefinition.value + "%";

    metric.append(metricLabel, metricValue);
    metrics.appendChild(metric);
  });

  const description = document.createElement("span");
  description.className = "relay-description";
  description.textContent = localized.description;

  const summary = document.createElement("span");
  summary.className = "relay-option-summary";
  summary.append(top, metrics, description);

  const meta = document.createElement("span");
  meta.className = "relay-meta";
  const badge = document.createElement("span");
  badge.className = "relay-badge";
  badge.textContent = localized.badge;
  const count = document.createElement("span");
  count.className = "relay-agent-count";
  count.textContent = t("relay.agentCount", { count: localized.agentCount });
  meta.append(badge, count);

  label.append(input, summary, meta);
  option.append(detailsButton, label);
  return option;
}

function renderRelays(relays) {
  if (!relays || relays.length === 0) {
    elements.relayOptions.replaceChildren();
    state.relayId = "";
    return;
  }
  if (
    !state.relayId ||
    !relays.some(function (relay) {
      return relay.id === state.relayId;
    })
  ) {
    state.relayId = relays[0].id;
  }
  elements.relayOptions.replaceChildren();
  relays.forEach(function (relay) {
    elements.relayOptions.appendChild(
      createRelayOption(relay, relay.id === state.relayId)
    );
  });
}

function relayById(relayId) {
  if (!state.bootstrap) {
    return null;
  }
  return state.bootstrap.relays.find(function (relay) {
    return relay.id === relayId;
  });
}

function setReadmeStatus(status, titleKey, copyKey) {
  elements.readmeStatus.hidden = false;
  elements.readmeStatus.dataset.status = status;
  elements.readmeStatus.querySelector("strong").textContent = t(titleKey);
  elements.readmeStatus.querySelector("p").textContent = t(copyKey);
  elements.readmeContent.hidden = true;
  elements.readmeContent.replaceChildren();
}

function renderReadmeDocument(readme) {
  if (!window.ReadmeRenderer) {
    setReadmeStatus("error", "readme.errorTitle", "readme.errorCopy");
    return;
  }
  elements.readmeFileName.textContent = readme.fileName;
  elements.readmeStatus.hidden = true;
  elements.readmeContent.hidden = false;
  window.ReadmeRenderer.render(
    elements.readmeContent,
    readme.content,
    readme.assets
  );
  elements.readmeContent.scrollTop = 0;
}

async function openReadme(relayId, focusCloseButton) {
  const relay = relayById(relayId);
  const localized = localizedRelay(relay);
  if (!relay || !localized) {
    return;
  }

  state.readmeRelayId = relayId;
  elements.readmeTitle.textContent = localized.name;
  elements.readmeLanguage.textContent = t(
    state.locale === "en" ? "readme.languageEn" : "readme.languageZh"
  );
  elements.readmeFileName.textContent = "README";

  if (!elements.readmeDialog.open) {
    if (typeof elements.readmeDialog.showModal === "function") {
      elements.readmeDialog.showModal();
    } else {
      elements.readmeDialog.setAttribute("open", "");
    }
  }
  if (focusCloseButton !== false) {
    elements.readmeCloseButton.focus();
  }

  if (!localized.readmeLocales.includes(state.locale)) {
    state.readmeRequestKey = "";
    setReadmeStatus(
      "unavailable",
      "readme.unavailableTitle",
      "readme.unavailableCopy"
    );
    return;
  }

  const cacheKey = relayId + ":" + state.locale;
  if (state.readmeCache.has(cacheKey)) {
    state.readmeRequestKey = cacheKey;
    renderReadmeDocument(state.readmeCache.get(cacheKey));
    return;
  }

  const requestKey = cacheKey + ":" + Date.now();
  state.readmeRequestKey = requestKey;
  setReadmeStatus("loading", "readme.loadingTitle", "readme.loadingCopy");
  try {
    const readme = await apiRequest("/api/readme", {
      relayId: relayId,
      locale: state.locale
    });
    state.readmeCache.set(cacheKey, readme);
    if (
      state.readmeRequestKey === requestKey &&
      elements.readmeDialog.open
    ) {
      renderReadmeDocument(readme);
    }
  } catch (_error) {
    if (
      state.readmeRequestKey === requestKey &&
      elements.readmeDialog.open
    ) {
      setReadmeStatus("error", "readme.errorTitle", "readme.errorCopy");
    }
  }
}

function closeReadmeDialog() {
  state.readmeRequestKey = "";
  if (typeof elements.readmeDialog.close === "function") {
    elements.readmeDialog.close();
  } else {
    elements.readmeDialog.removeAttribute("open");
    state.readmeRelayId = "";
  }
}

function renderRelayDetectionList(container, detections) {
  container.replaceChildren();
  detections.forEach(function (detection) {
    const item = document.createElement("section");
    item.className = "conflict-item";

    const heading = document.createElement("div");
    heading.className = "conflict-item-heading";
    const name = document.createElement("strong");
    name.textContent = relayNameById(detection.id, detection.name);
    const status = document.createElement("span");
    status.textContent = t(
      detection.status === "installed" ? "dialog.installed" : "dialog.partial"
    );
    heading.append(name, status);

    const paths = document.createElement("ul");
    detection.paths.forEach(function (path) {
      const listItem = document.createElement("li");
      listItem.textContent = path;
      paths.appendChild(listItem);
    });
    item.append(heading, paths);
    container.appendChild(item);
  });
}

function renderConflictList(inspection) {
  renderRelayDetectionList(elements.conflictList, inspection.conflicts);
}

function renderConflictDialog(inspection) {
  renderConflictList(inspection);
  if (
    !elements.conflictDialog.open &&
    typeof elements.conflictDialog.showModal === "function"
  ) {
    elements.conflictDialog.showModal();
  } else if (!elements.conflictDialog.open) {
    elements.conflictDialog.setAttribute("open", "");
  }
  elements.cancelConflictButton.focus();
}

function closeConflictDialog() {
  if (typeof elements.conflictDialog.close === "function") {
    elements.conflictDialog.close();
  } else {
    elements.conflictDialog.removeAttribute("open");
  }
}

function renderRemovalDialog(inspection) {
  state.removalInspection = inspection;
  elements.removeTargetPath.textContent = inspection.targetRoot;
  renderRelayDetectionList(elements.removeRelayList, inspection.installations);
  if (
    !elements.removeDialog.open &&
    typeof elements.removeDialog.showModal === "function"
  ) {
    elements.removeDialog.showModal();
  } else if (!elements.removeDialog.open) {
    elements.removeDialog.setAttribute("open", "");
  }
  elements.cancelRemoveButton.focus();
}

function closeRemovalDialog() {
  if (typeof elements.removeDialog.close === "function") {
    elements.removeDialog.close();
  } else {
    elements.removeDialog.removeAttribute("open");
    state.removalInspection = null;
  }
}

async function inspectSelection() {
  if (!validateProjectPath()) {
    return null;
  }
  setBusy(true, "install.checking");
  try {
    const inspection = await apiRequest("/api/inspect", installPayload(false));
    updatePreflight(inspection);
    return inspection;
  } finally {
    setBusy(false, "install.button");
  }
}

async function inspectRemoval() {
  if (!validateProjectPath()) {
    return null;
  }
  setBusy(true, "remove.inspecting", "remove");
  try {
    return await apiRequest("/api/remove/inspect", targetPayload());
  } finally {
    setBusy(false, "scope.removeButton", "remove");
  }
}

function collisionDetails(inspection) {
  if (!inspection || inspection.unmanagedCollisions.length === 0) {
    return "";
  }
  return (
    t("result.paths") + ": " + inspection.unmanagedCollisions.join(" · ")
  );
}

async function runInstall(removeConflicts) {
  setBusy(true, "install.installing");
  clearResult();
  try {
    const result = await apiRequest(
      "/api/install",
      installPayload(removeConflicts)
    );
    closeConflictDialog();
    setResult({
      status: "success",
      kind: "installSuccess",
      data: result
    });
    const refreshed = await apiRequest("/api/inspect", installPayload(false));
    updatePreflight(refreshed);
  } catch (error) {
    if (
      error instanceof ApiError &&
      error.code === "relay_conflict" &&
      error.details
    ) {
      updatePreflight(error.details);
      renderConflictDialog(error.details);
      return;
    }
    if (
      error instanceof ApiError &&
      error.code === "unmanaged_collision" &&
      error.details
    ) {
      closeConflictDialog();
      updatePreflight(error.details);
      setResult({
        status: "error",
        kind: "error",
        titleKey: "result.blockedTitle",
        messageKey: "result.blockedCopy",
        details: collisionDetails(error.details)
      });
      return;
    }
    closeConflictDialog();
    setResult({
      status: "error",
      kind: "error",
      titleKey: "result.installFailTitle",
      error: error
    });
  } finally {
    setBusy(false, "install.button");
  }
}

async function runRemoval() {
  setBusy(true, "remove.removing", "remove");
  clearResult();
  try {
    const result = await apiRequest("/api/remove", targetPayload());
    closeRemovalDialog();
    if (result.removedRelays.length === 0) {
      setResult({
        status: "success",
        kind: "message",
        titleKey: "result.removeEmptyTitle",
        messageKey: "result.removeEmptyCopy"
      });
    } else {
      setResult({
        status: "success",
        kind: "removeSuccess",
        data: result
      });
    }
    const refreshed = await apiRequest("/api/inspect", installPayload(false));
    updatePreflight(refreshed);
  } catch (error) {
    closeRemovalDialog();
    setResult({
      status: "error",
      kind: "error",
      titleKey: "result.removeFailTitle",
      error: error
    });
  } finally {
    setBusy(false, "scope.removeButton", "remove");
  }
}

function updateConfigPathButton() {
  elements.configPathButton.textContent = t(
    elements.configPath.hidden ? "config.button" : "config.hide"
  );
}

async function initialize() {
  initializeLanguage();
  initializeTheme();
  try {
    const response = await fetch("/api/bootstrap", { cache: "no-store" });
    const payload = await response.json();
    if (!response.ok || !payload.ok) {
      throw new ApiError(payload.error, response.status);
    }
    state.bootstrap = payload.data;
    state.sessionToken = payload.data.sessionToken;
    elements.projectPathInput.value = payload.data.defaultProjectPath;
    elements.globalTargetPath.textContent = payload.data.globalPath;
    elements.configPath.textContent = payload.data.configPath;
    renderRelays(payload.data.relays);
    updateSummary();
    setBusy(false, "install.button");
  } catch (error) {
    setBusy(false, "install.unavailable");
    elements.installButton.disabled = true;
    setResult({
      status: "error",
      kind: "error",
      titleKey: "result.initFailTitle",
      messageKey: "result.initFailCopy",
      error: error
    });
    setSummaryState("warning", "summary.unavailable");
    return;
  }

  try {
    const inspection = await apiRequest("/api/inspect", installPayload(false));
    updatePreflight(inspection);
  } catch (error) {
    setResult({
      status: "error",
      kind: "error",
      titleKey: "result.initialCheckTitle",
      error: error,
      details: t("result.initialCheckHint")
    });
    updatePreflight(null);
  }
}

elements.themeToggle.addEventListener("click", function () {
  const current = document.documentElement.dataset.theme;
  setTheme(current === "dark" ? "light" : "dark");
});

elements.languageOptions.forEach(function (button) {
  button.addEventListener("click", function () {
    if (button.dataset.locale !== state.locale) {
      applyLanguage(button.dataset.locale, true);
    }
  });
});

document.querySelectorAll('input[name="scope"]').forEach(function (input) {
  input.addEventListener("change", function () {
    if (!input.checked) {
      return;
    }
    state.scope = input.value;
    const isProject = state.scope === "project";
    elements.globalTargetField.hidden = isProject;
    elements.projectPathField.hidden = !isProject;
    clearPathError();
    clearResult();
    state.removalInspection = null;
    updateSummary();
    updatePreflight(null);
    if (isProject) {
      elements.projectPathInput.focus();
    }
  });
});

elements.projectPathInput.addEventListener("input", function () {
  state.projectPath = elements.projectPathInput.value;
  clearPathError();
  clearResult();
  state.removalInspection = null;
  updateSummary();
  updatePreflight(null);
});

elements.projectPathInput.addEventListener("blur", function () {
  if (state.scope === "project" && elements.projectPathInput.value.trim()) {
    validateProjectPath();
  }
});

elements.browseButton.addEventListener("click", async function () {
  setBusy(true, "install.waiting");
  clearPathError();
  try {
    const result = await apiRequest("/api/browse", {
      initialPath: elements.projectPathInput.value.trim(),
      locale: state.locale
    });
    if (result.path) {
      elements.projectPathInput.value = result.path;
      state.projectPath = result.path;
      updateSummary();
      updatePreflight(null);
      elements.projectPathInput.focus();
    }
  } catch (error) {
    setResult({
      status: "error",
      kind: "error",
      titleKey: "result.browseFailTitle",
      error: error
    });
  } finally {
    setBusy(false, "install.button");
  }
});

elements.removeRelaysButton.addEventListener("click", async function () {
  if (state.busy || !state.bootstrap || !validateProjectPath()) {
    return;
  }
  clearResult();
  try {
    const inspection = await inspectRemoval();
    if (!inspection) {
      return;
    }
    state.removalInspection = inspection;
    if (!inspection.canRemove) {
      state.removalInspection = null;
      setResult({
        status: "success",
        kind: "message",
        titleKey: "result.removeEmptyTitle",
        messageKey: "result.removeEmptyCopy"
      });
      return;
    }
    renderRemovalDialog(inspection);
  } catch (error) {
    setResult({
      status: "error",
      kind: "error",
      titleKey: "result.removeFailTitle",
      error: error
    });
  }
});

elements.form.addEventListener("submit", async function (event) {
  event.preventDefault();
  if (state.busy || !validateProjectPath()) {
    return;
  }
  clearResult();
  try {
    const inspection = await inspectSelection();
    if (!inspection) {
      return;
    }
    if (inspection.unmanagedCollisions.length > 0) {
      setResult({
        status: "error",
        kind: "error",
        titleKey: "result.blockedTitle",
        messageKey: "result.blockedCopy",
        details: collisionDetails(inspection)
      });
      return;
    }
    if (inspection.conflicts.length > 0) {
      renderConflictDialog(inspection);
      return;
    }
    await runInstall(false);
  } catch (error) {
    setResult({
      status: "error",
      kind: "error",
      titleKey: "result.checkFailTitle",
      error: error
    });
  }
});

elements.cancelConflictButton.addEventListener("click", function () {
  closeConflictDialog();
  elements.installButton.focus();
});

elements.confirmConflictButton.addEventListener("click", function () {
  if (!state.busy) {
    runInstall(true);
  }
});

elements.cancelRemoveButton.addEventListener("click", function () {
  closeRemovalDialog();
  elements.removeRelaysButton.focus();
});

elements.confirmRemoveButton.addEventListener("click", function () {
  if (!state.busy && state.removalInspection) {
    runRemoval();
  }
});

elements.removeDialog.addEventListener("close", function () {
  state.removalInspection = null;
  if (!state.busy) {
    elements.removeRelaysButton.focus();
  }
});

elements.readmeCloseButton.addEventListener("click", function () {
  closeReadmeDialog();
});

elements.readmeDialog.addEventListener("close", function () {
  state.readmeRelayId = "";
  state.readmeRequestKey = "";
});

elements.configPathButton.addEventListener("click", function () {
  elements.configPath.hidden = !elements.configPath.hidden;
  updateConfigPathButton();
});

initialize();
