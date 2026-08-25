"use strict";

(function () {
  const inlineTokenPattern =
    /(`[^`\n]+`|\*\*[^*\n]+\*\*|\*[^*\n]+\*|\[[^\]]+\]\([^)]+\))/g;

  function appendLink(parent, label, target) {
    if (target.startsWith("#")) {
      const link = document.createElement("a");
      link.href = target;
      link.textContent = label;
      link.addEventListener("click", function (event) {
        event.preventDefault();
        const targetId = decodeURIComponent(target.slice(1));
        const heading = document.getElementById(targetId);
        if (heading) {
          heading.scrollIntoView({ block: "start" });
          heading.focus({ preventScroll: true });
        }
      });
      parent.appendChild(link);
      return;
    }

    if (/^https?:\/\//i.test(target)) {
      const link = document.createElement("a");
      link.href = target;
      link.target = "_blank";
      link.rel = "noreferrer noopener";
      link.textContent = label;
      parent.appendChild(link);
      return;
    }

    const localReference = document.createElement("span");
    localReference.className = "readme-local-reference";
    localReference.textContent = label;
    localReference.title = target;
    parent.appendChild(localReference);
  }

  function appendInline(parent, text) {
    const tokenPattern = new RegExp(inlineTokenPattern.source, "g");
    let cursor = 0;
    let match = tokenPattern.exec(text);
    while (match) {
      if (match.index > cursor) {
        parent.appendChild(
          document.createTextNode(text.slice(cursor, match.index))
        );
      }
      const token = match[0];
      if (token.startsWith("`")) {
        const code = document.createElement("code");
        code.textContent = token.slice(1, -1);
        parent.appendChild(code);
      } else if (token.startsWith("**")) {
        const strong = document.createElement("strong");
        appendInline(strong, token.slice(2, -2));
        parent.appendChild(strong);
      } else if (token.startsWith("*")) {
        const emphasis = document.createElement("em");
        appendInline(emphasis, token.slice(1, -1));
        parent.appendChild(emphasis);
      } else {
        const linkMatch = /^\[([^\]]+)\]\(([^)\s]+)(?:\s+"[^"]*")?\)$/.exec(
          token
        );
        if (linkMatch) {
          appendLink(parent, linkMatch[1], linkMatch[2]);
        } else {
          parent.appendChild(document.createTextNode(token));
        }
      }
      cursor = match.index + token.length;
      match = tokenPattern.exec(text);
    }
    if (cursor < text.length) {
      parent.appendChild(document.createTextNode(text.slice(cursor)));
    }
  }

  function slugify(value) {
    return value
      .trim()
      .toLocaleLowerCase()
      .replace(/[^\p{L}\p{N}\s-]/gu, "")
      .replace(/\s+/g, "-")
      .replace(/-+/g, "-")
      .replace(/^-|-$/g, "");
  }

  function uniqueSlug(value, usedSlugs) {
    const base = slugify(value) || "section";
    let slug = base;
    let suffix = 2;
    while (usedSlugs.has(slug)) {
      slug = base + "-" + suffix;
      suffix += 1;
    }
    usedSlugs.add(slug);
    return slug;
  }

  function appendImage(parent, source, altText, assets) {
    const resolvedSource = assets[source];
    if (!resolvedSource) {
      const fallback = document.createElement("span");
      fallback.className = "readme-image-fallback";
      fallback.textContent = altText || source;
      parent.appendChild(fallback);
      return;
    }
    const image = document.createElement("img");
    image.className = "readme-image";
    image.src = resolvedSource;
    image.alt = altText || "";
    image.loading = "lazy";
    image.decoding = "async";
    parent.appendChild(image);
  }

  function cloneSafeHtmlNode(source, target, assets) {
    if (source.nodeType === Node.TEXT_NODE) {
      target.appendChild(document.createTextNode(source.textContent || ""));
      return;
    }
    if (source.nodeType !== Node.ELEMENT_NODE) {
      return;
    }

    const tag = source.tagName.toLowerCase();
    if (tag === "br") {
      target.appendChild(document.createElement("br"));
      return;
    }
    if (tag === "img") {
      appendImage(
        target,
        source.getAttribute("src") || "",
        source.getAttribute("alt") || "",
        assets
      );
      return;
    }
    if (tag === "a") {
      appendLink(
        target,
        source.textContent || "",
        source.getAttribute("href") || ""
      );
      return;
    }

    const allowedTags = new Set(["strong", "em", "code"]);
    const destination = allowedTags.has(tag)
      ? document.createElement(tag)
      : document.createDocumentFragment();
    Array.from(source.childNodes).forEach(function (child) {
      cloneSafeHtmlNode(child, destination, assets);
    });
    target.appendChild(destination);
  }

  function appendHtmlParagraph(container, html, assets) {
    const parsed = new DOMParser().parseFromString(html, "text/html");
    const sourceParagraph = parsed.body.querySelector("p");
    if (!sourceParagraph) {
      return;
    }
    const alignment = (sourceParagraph.getAttribute("align") || "").toLowerCase();
    if (alignment === "right") {
      return;
    }
    const paragraph = document.createElement("p");
    if (alignment === "center") {
      paragraph.className = "readme-align-center";
    }
    Array.from(sourceParagraph.childNodes).forEach(function (child) {
      cloneSafeHtmlNode(child, paragraph, assets);
    });
    if (paragraph.childNodes.length > 0) {
      container.appendChild(paragraph);
    }
  }

  function splitTableRow(line) {
    return line
      .trim()
      .replace(/^\|/, "")
      .replace(/\|$/, "")
      .split("|")
      .map(function (cell) {
        return cell.trim();
      });
  }

  function isTableDivider(line) {
    const cells = splitTableRow(line);
    return (
      cells.length > 0 &&
      cells.every(function (cell) {
        return /^:?-{3,}:?$/.test(cell);
      })
    );
  }

  function isListLine(line) {
    return /^\s*(?:[-*+] |\d+\. )/.test(line);
  }

  function isBlockStart(lines, index) {
    const line = lines[index] || "";
    return (
      /^```/.test(line) ||
      /^#{1,6}\s+/.test(line) ||
      /^>\s?/.test(line) ||
      isListLine(line) ||
      /^<p\b/i.test(line) ||
      /^\s*(?:---+|\*\*\*+)\s*$/.test(line) ||
      (line.includes("|") && isTableDivider(lines[index + 1] || ""))
    );
  }

  function render(container, markdown, assets) {
    const assetMap = assets && typeof assets === "object" ? assets : {};
    const lines = String(markdown || "")
      .replace(/\r\n?/g, "\n")
      .split("\n");
    const fragment = document.createDocumentFragment();
    const usedSlugs = new Set();
    let index = 0;

    while (index < lines.length) {
      const line = lines[index];
      if (!line.trim()) {
        index += 1;
        continue;
      }

      if (/^<p\b/i.test(line)) {
        const htmlLines = [line];
        while (
          index + 1 < lines.length &&
          !/<\/p>\s*$/i.test(htmlLines[htmlLines.length - 1])
        ) {
          index += 1;
          htmlLines.push(lines[index]);
        }
        appendHtmlParagraph(fragment, htmlLines.join("\n"), assetMap);
        index += 1;
        continue;
      }

      const fenceMatch = /^```([^\s]*)\s*$/.exec(line);
      if (fenceMatch) {
        const codeLines = [];
        index += 1;
        while (index < lines.length && !/^```\s*$/.test(lines[index])) {
          codeLines.push(lines[index]);
          index += 1;
        }
        if (index < lines.length) {
          index += 1;
        }
        const pre = document.createElement("pre");
        const code = document.createElement("code");
        if (fenceMatch[1]) {
          code.dataset.language = fenceMatch[1];
        }
        code.textContent = codeLines.join("\n");
        pre.appendChild(code);
        fragment.appendChild(pre);
        continue;
      }

      const headingMatch = /^(#{1,6})\s+(.+)$/.exec(line);
      if (headingMatch) {
        const level = Math.max(3, Math.min(6, headingMatch[1].length + 1));
        const heading = document.createElement("h" + level);
        heading.id = uniqueSlug(headingMatch[2], usedSlugs);
        heading.tabIndex = -1;
        appendInline(heading, headingMatch[2]);
        fragment.appendChild(heading);
        index += 1;
        continue;
      }

      if (line.includes("|") && isTableDivider(lines[index + 1] || "")) {
        const headers = splitTableRow(line);
        index += 2;
        const rows = [];
        while (index < lines.length && /^\s*\|/.test(lines[index])) {
          rows.push(splitTableRow(lines[index]));
          index += 1;
        }
        const wrapper = document.createElement("div");
        wrapper.className = "readme-table-wrap";
        const table = document.createElement("table");
        const head = document.createElement("thead");
        const headRow = document.createElement("tr");
        headers.forEach(function (cell) {
          const heading = document.createElement("th");
          heading.scope = "col";
          appendInline(heading, cell);
          headRow.appendChild(heading);
        });
        head.appendChild(headRow);
        table.appendChild(head);
        const body = document.createElement("tbody");
        rows.forEach(function (row) {
          const tableRow = document.createElement("tr");
          row.forEach(function (cell) {
            const data = document.createElement("td");
            appendInline(data, cell);
            tableRow.appendChild(data);
          });
          body.appendChild(tableRow);
        });
        table.appendChild(body);
        wrapper.appendChild(table);
        fragment.appendChild(wrapper);
        continue;
      }

      if (isListLine(line)) {
        const ordered = /^\s*\d+\. /.test(line);
        const list = document.createElement(ordered ? "ol" : "ul");
        while (index < lines.length && isListLine(lines[index])) {
          const currentOrdered = /^\s*\d+\. /.test(lines[index]);
          if (currentOrdered !== ordered) {
            break;
          }
          const item = document.createElement("li");
          appendInline(
            item,
            lines[index].replace(/^\s*(?:[-*+] |\d+\. )/, "")
          );
          list.appendChild(item);
          index += 1;
        }
        fragment.appendChild(list);
        continue;
      }

      if (/^>\s?/.test(line)) {
        const quoteLines = [];
        while (index < lines.length && /^>\s?/.test(lines[index])) {
          quoteLines.push(lines[index].replace(/^>\s?/, ""));
          index += 1;
        }
        const quote = document.createElement("blockquote");
        appendInline(quote, quoteLines.join(" "));
        fragment.appendChild(quote);
        continue;
      }

      if (/^\s*(?:---+|\*\*\*+)\s*$/.test(line)) {
        fragment.appendChild(document.createElement("hr"));
        index += 1;
        continue;
      }

      const paragraphLines = [line.trim()];
      index += 1;
      while (
        index < lines.length &&
        lines[index].trim() &&
        !isBlockStart(lines, index)
      ) {
        paragraphLines.push(lines[index].trim());
        index += 1;
      }
      const paragraph = document.createElement("p");
      appendInline(paragraph, paragraphLines.join(" "));
      fragment.appendChild(paragraph);
    }

    container.replaceChildren(fragment);
  }

  window.ReadmeRenderer = Object.freeze({ render: render });
})();
