import { combineReducers } from "redux"
import reduceTodos from './features/todos.js'
import reduceFilters from './features/filters.js'

const rootReducer = combineReducers({
    todos: reduceTodos, filtrers: reduceFilters
})

export default rootReducer
