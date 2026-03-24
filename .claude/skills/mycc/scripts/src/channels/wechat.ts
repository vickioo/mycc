/**
 * WechatChannel - 微信小程序消息通道
 *
 * 在 WebChannel 基础上，对文本内容进行 Markdown → 纯文本转换，
 * 确保微信小程序能正确显示 Claude 的回复。
 */

import { ServerResponse } from 'http';
import type { SSEEvent } from '../adapters/interface.js';
import type { MessageChannel } from './interface.js';
import { convertToPlainText } from './markdown-converter.js';

export interface WechatChannelConfig {
  res: ServerResponse;
}

export class WechatChannel implements MessageChannel {
  readonly id = "wechat";
  private res: ServerResponse;
  private sessionId?: string;

  constructor(config: WechatChannelConfig) {
    this.res = config.res;
  }

  setSessionId(sessionId: string): void {
    this.sessionId = sessionId;
  }

  getSessionId(): string | undefined {
    return this.sessionId;
  }

  async send(event: SSEEvent): Promise<void> {
    // 先从事件中提取 session_id（如果存在）
    if (event && typeof event === "object" && "type" in event) {
      if (event.type === "system" && "session_id" in event) {
        this.sessionId = event.session_id as string;
      }
    }
    // 转换文本
    const transformed = this.transformEvent(event);
    const data = JSON.stringify(transformed);
    this.res.write('data: ' + data + '\n\n');
  }

  async sendDone(): Promise<void> {
    await this.send({ type: 'done', sessionId: this.sessionId } as SSEEvent);
    this.res.end();
  }

  async sendError(error: string): Promise<void> {
    await this.send({ type: 'error', error } as SSEEvent);
    this.res.end();
  }

  private transformEvent(event: SSEEvent): SSEEvent {
    const copy: any = { ...event };

    if (event.type === 'text' && 'text' in event) {
      copy.text = convertToPlainText(String(event.text ?? ''));
    } else if (event.type === 'content_block_delta' && 'delta' in event) {
      const delta = event.delta as any;
      if (delta && 'text' in delta) {
        copy.delta = { ...delta, text: convertToPlainText(String(delta.text)) };
      }
    } else if (event.type === 'assistant' && 'message' in event) {
      const msg = event.message as any;
      if (msg && 'content' in msg && Array.isArray(msg.content)) {
        copy.message = {
          ...msg,
          content: msg.content.map((block: any) => {
            if (block.type === 'text') {
              return { ...block, text: convertToPlainText(block.text) };
            }
            return block;
          })
        };
      }
    }
    return copy;
  }
}
