import React, { useEffect } from 'react';
import { RealtimeClient } from '@openai/realtime-api-beta';

function App() {
  useEffect(() => {
    const client = new RealtimeClient({
      apiKey: process.env.OPENAI_API_KEY,
      dangerouslyAllowAPIKeyInBrowser: true, // 注意: セキュリティ上のリスクがあります
    });

    client.updateSession({ instructions: 'You are a great, upbeat friend.' });
    client.updateSession({ voice: 'alloy' });
    client.updateSession({
      turn_detection: { type: 'none' },
      input_audio_transcription: { model: 'whisper-1' },
    });

    client.on('conversation.updated', (event) => {
      const { item, delta } = event;
      const items = client.conversation.getItems();
      console.log('Conversation updated:', items);
    });

    client.connect().then(() => {
      client.sendUserMessageContent([{ type: 'input_text', text: `How are you?` }]);
    });

  }, []);

  return (
    <div className="App">
      <h1>OpenAI Realtime API Demo</h1>
    </div>
  );
}

export default App;
