import { DataType } from "@renderer/data";
import { create } from "zustand";
interface StateProps{
    data: DataType[],
    setData: (data: DataType[]) => void,
    search: string,
    setSearch: (search: string) => void
}
export const useStore = create<StateProps>((set) => ({
    data: [],
    setData: (data) => set({data}),
    search: "",
    setSearch: (search) => set({search})
  }))

