'use server';

import { createAI, getMutableAIState, streamUI } from 'ai/rsc';
import { createAzure } from '@ai-sdk/azure';
import { ReactNode } from 'react';
import { z } from 'zod';
import { generateId } from 'ai';
import { Stock } from '@/components/Stock';

export interface ServerMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ClientMessage {
  id: string;
  role: 'user' | 'assistant';
  display: ReactNode;
}

export async function continueConversation(
  input: string,
): Promise<ClientMessage> {
  'use server';

  const history = getMutableAIState();

  const azure = createAzure({
    resourceName: <your aoai resourse name>,
    apiKey: <your aoai key>,
  });

  const result = await streamUI({
    model: azure('gpt-4o'),
    messages: [...history.get(), { role: 'user', content: input }],
    text: ({ content, done }) => {
      if (done) {
        history.done((messages: ServerMessage[]) => [
          ...messages,
          { role: 'assistant', content },
        ]);
      }

      return <div>{content}</div>;
    },
    tools: {
      showStockInformation: {
        description:
          'Get stock information for symbol for the last numOfMonths months',
        parameters: z.object({
          symbol: z
            .string()
            .describe('The stock symbol to get information for'),
          numOfMonths: z
            .number()
            .describe('The number of months to get historical information for'),
        }),
        generate: async ({ symbol, numOfMonths }) => {
          history.done((messages: ServerMessage[]) => [
            ...messages,
            {
              role: 'assistant',
              content: `Showing stock information for ${symbol}`,
            },
          ]);

          return <Stock symbol={symbol} numOfMonths={numOfMonths} />;
        },
      },
    },
  });

  return {
    id: generateId(),
    role: 'assistant',
    display: result.value,
  };
}

export const AI = createAI<ServerMessage[], ClientMessage[]>({
  actions: {
    continueConversation,
  },
  initialAIState: [],
  initialUIState: [],
});