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
    code: string,
    setCode: (code: string) => void
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
    code: "",
    setCode: (code) => set({code})
  }))


