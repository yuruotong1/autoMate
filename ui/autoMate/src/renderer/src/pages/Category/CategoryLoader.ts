export default () => {
    return window.api.sql("SELECT * FROM categories", "findAll")
}