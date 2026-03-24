/**
 * Markdown → 纯文本转换器（微信/手机端优化版）
 *
 * 小红书风格输出：emoji 标号、短行、自动软换行
 */

import { marked } from 'marked';

export function convertToPlainText(markdown: string): string {
  if (!markdown) return '';
  try {
    const tokens = marked.lexer(markdown);
    let result = '';
    for (const token of tokens) {
      result += tokenToText(token);
    }
    return result.trim();
  } catch (error) {
    console.warn('[markdown-converter] 转换失败:', error);
    return markdown;
  }
}

function tokenToText(token: any): string {
  switch (token.type) {
    case 'text':
      return token.raw + '\n';

    case 'space':
      return ' ';

    case 'br':
      return '\n';

    case 'paragraph': {
      const inner = token.tokens ? token.tokens.map(tokenToText).join('') : '';
      return wrapLines(inner) + '\n\n';
    }

    // 标题：🔖 大号数字
    case 'heading': {
      const depth = Math.min(token.depth, 4);
      const underline = '\u2500'.repeat(depth * 3);
      const text = token.tokens ? token.tokens.map(tokenToText).join('').trim() : '';
      return '\n\uD83C\uDD97 ' + text + '\n' + underline + '\n\n';
    }

    // 列表：✅ 🔹 🔸 序号
    case 'list': {
      let t = '\n';
      token.items?.forEach((item: any, idx: number) => {
        const task = item.task;
        const checked = item.checked;
        let bullet: string;
        if (task === true && checked === false) bullet = '\u2705';     // todo 未完成
        else if (task === true && checked === true) bullet = '\u274C';    // todo 已完成
        else if (token.ordered)    bullet = String.fromCharCode(0x2460 + idx) + '.';
        else                      bullet = '\uD83D\uDDD8';             // 无序 bullet
        const content = item.tokens ? item.tokens.map(tokenToText).join('').trim() : '';
        t += '  ' + bullet + ' ' + wrapLines(content) + '\n';
      });
      return t + '\n';
    }

    // 引用：💬 前缀
    case 'blockquote': {
      const inner = token.tokens ? token.tokens.map(tokenToText).join('').trim() : '';
      return '  \uD83D\uDCAC ' + inner.replace(/\n/g, '\n    ') + '\n\n';
    }

    // 代码块：保留但去掉语言标记前缀
    case 'code': {
      return '\n\uD83D\uDCBB 代码:\n' + (token.text || token.raw || '') + '\n\u2500'.repeat(12) + '\n\n';
    }

    // 行内代码：加点样式
    case 'codespan':
      return ' \u2B50' + token.text + '\u2B50 ';

    // 表格：小红书 key:value 流式条列
    case 'table': {
      const headers = token.header?.map((c: any) => cellText(c).trim()) || [];
      const rows = token.rows?.map((row: any[]) =>
        row.map((c: any) => cellText(c).trim())
      ) || [];
      if (!headers.length) return '';
      let t = '\n  \uD83D\uDCCB 表格\n  \u2500'.repeat(6) + '\n';
      // 表头一行
      t += '  ';
      headers.forEach((h: string, i: number) => {
        t += '\u2B50' + h + '  ';
      });
      t += '\n  \u2500'.repeat(6) + '\n';
      // 每行数据
      rows.forEach((row: any[], ri: number) => {
        t += '  \uD83D\uDD39 ' + (ri + 1) + '.\n';
        row.forEach((cell: string, ci: number) => {
          const key = headers[ci] || ('列' + (ci + 1));
          const wrapped = wrapLines(cell.trim(), 16);
          t += '     \uD83D\uDD38 ' + key + ': ' + wrapped + '\n';
        });
        t += '\n';
      });
      return t;
    }

    // 链接：显示文字 + 圆括号链接
    case 'link': {
      const text = token.tokens ? token.tokens.map(tokenToText).join('') : '';
      return token.href ? text + ' (' + token.href + ')' : text;
    }

    case 'image':
      return '\uD83D\uDDBC 图片: ' + (token.text || token.alt || '') + '\n';

    // 斜体/粗体/删除：直接取文本，不递归（避免内层 text token 加多余换行）
    case 'em':
    case 'strong':
    case 'del':
      return token.text || '';

    // 分隔线
    case 'hr':
      return '\n\u2500'.repeat(10) + '\n\n';

    // HTML：去标签
    case 'html':
      return token.raw.replace(/<[^>]+>/g, '') + '\n';

    default:
      if (token.tokens) return token.tokens.map(tokenToText).join('');
      if (token.text) return token.text;
      return '';
  }
}

function cellText(cell: any): string {
  if (!cell) return '';
  if (cell.tokens) return cell.tokens.map(tokenToText).join('');
  if (cell.text) return cell.text;
  return '';
}

/**
 * 软换行：超过 maxLen 字符的文本自动在空格处截断，
 * 每行加 4 个空格缩进，保持手机端阅读宽度
 */
function wrapLines(text: string, maxLen: number = 22): string {
  if (!text) return '';
  const result: string[] = [];
  const paragraphs = text.split(/\n{2,}/);
  for (const para of paragraphs) {
    if (para.length <= maxLen) {
      result.push(para);
    } else {
      // 先尝试按空格软截断
      const words = para.split(/(\s+)/);
      let line = '';
      for (const w of words) {
        if ((line + w).length > maxLen && line.length > 0) {
          result.push(line.trim());
          line = '    ' + w;
        } else {
          line += w;
        }
      }
      if (line.trim()) result.push(line.trim());
      // 如果上面的结果只有一行（说明没有空格），按固定长度硬截断
      if (result.length === 0 || (result.length === 1 && para.length > maxLen)) {
        result.length = 0;
        for (let i = 0; i < para.length; i += maxLen) {
          result.push(para.slice(i, i + maxLen));
        }
      }
    }
  }
  return result.join('\n     ');
}
