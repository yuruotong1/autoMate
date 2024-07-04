import { ChatMessage } from "@ant-design/pro-chat";
import { create } from "zustand";
interface StateProps{
    data: ContentType[],
    setData: (data: ContentType[]) => void,
    search: string,
    setSearch: (search: string) => void,
    error: string,
    setError: (error: string) => void,
    selectId: number,
    setSelectId: (selectId: number) => void,
    editCategoryId: number,
    setEditCategoryId: (id: number) => void,
    chatMessages: ChatMessage<Record<string, any>>[],
    setChatMessage: (chatMessage: ChatMessage<Record<string, any>>[]) => void,
    isCodeLoading: boolean,
    setIsCodeLoading: (isCodeLoading: boolean) => void,
    sendChatWithSearch: string,
    setSendChatWithSearch: (sendChatWithSearch: string) => void
}
export const useStore = create<StateProps>((set) => ({
    data: [],
    setData: (data) => set({data}),
    search: "",
    setSearch: (search) => set({search}),
    error: "",
    setError: (error) => set({error}),
    selectId: 0,
    setSelectId: (selectId) => set({selectId}),
    editCategoryId: 0,
    setEditCategoryId: (editCategoryId) => set({editCategoryId}),
    chatMessages: [],
    setChatMessage: (chatMessages) => set({chatMessages}),
    isCodeLoading: false,
    setIsCodeLoading: (isCodeLoading) => set({isCodeLoading}),
    sendChatWithSearch: '',
    setSendChatWithSearch: (sendChatWithSearch) => set({sendChatWithSearch})
  }))


