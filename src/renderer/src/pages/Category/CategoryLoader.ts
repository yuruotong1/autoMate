export default () => {
    return window.api.sql("SELECT * FROM categories order by id desc", "findAll")
}