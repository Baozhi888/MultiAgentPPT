import uuid
import httpx
from a2a.client import A2AClient
import asyncio
from a2a.types import (MessageSendParams, SendMessageRequest, SendStreamingMessageRequest)

async def httpx_client():
    timeout = httpx.Timeout(30.0)  # 设置为 30 秒
    async with httpx.AsyncClient(timeout=timeout) as httpx_client:
        # 初始化客户端（确保base_url包含协议头）
        client = await A2AClient.get_client_from_agent_card_url(
            httpx_client, 'http://localhost:10001'  # 确保此处是完整 URL
        )

        # 生成唯一请求ID
        request_id = uuid.uuid4().hex
        # 构造消息参数
        send_message_payload = {
            'message': {
                'role': 'user',
                'parts': [{'type': 'text', 'text': prompt}],
                'messageId': request_id
            }
        }
        # 流式请求的示例
        streaming_request = SendStreamingMessageRequest(
            params=MessageSendParams(**send_message_payload)  # 同样的 payload 可以用于非流式请求
        )

        stream_response = client.send_message_streaming(streaming_request)
        async for chunk in stream_response:
            print(chunk.model_dump(mode='json', exclude_none=True))

if __name__ == '__main__':
    prompt = """我想调研电动汽车发展"""
    asyncio.run(httpx_client())
