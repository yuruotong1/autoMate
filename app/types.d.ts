type SqlActionType = 'findAll' | 'findOne' | 'create' | 'update' | 'del'|'config'

type CategoryType = {
    id: number
    name: string
    createdAt: string
}

type ContentType = {
    id: number
    title: string
    content: string
    category_id: string
    created_at: string
}


type WindowNameType = 'search' | 'config' | 'code' | 'interactive'

type ConfigType = {
    id: number
    content: string
}


type ConfigDataType = {
    shortCut: string
    llm: {
        model: string
        apiKey: string
        baseURL: string
    }
}


type LLM = {
    model: string
    apiKey: string
    baseURL: string
}