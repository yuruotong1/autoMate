import { ChatMessage } from "@ant-design/pro-chat";
import { create } from "zustand";
interface StateProps{
    error: string,
    setError: (error: string) => void,
    chatMessages: ChatMessage<Record<string, any>>[],
    setChatMessage: (chatMessage: ChatMessage<Record<string, any>>[]) => void,

}
export const useStore = create<StateProps>((set) => ({
    error: "",
    setError: (error) => set({error}),
    chatMessages: [],
    setChatMessage: (chatMessages) => set({chatMessages}),
  }))


