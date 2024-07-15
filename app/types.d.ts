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


type WindowNameType = 'search' | 'setting' | 'code' | 'interactive' | 'about'

type ConfigType = {
    id: number
    content: string
}


type ConfigDataType = {
    shortcut: string
    format: string
    llm: {
        model: string
        api_key?: string
        base_url?: string
        api_base?: string
    }
}
