import { combineReducers } from "redux"
import reduceTodos from './features/todos'
import reduceFilters from './features/filters'

const rootReducer = combineReducers({
    todos: reduceTodos, filtrers: reduceFilters
})

export default rootReducer
