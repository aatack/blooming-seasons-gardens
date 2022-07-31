import React from "react";
import { useSelector, useDispatch, Provider } from "react-redux";
import ReactDOM from "react-dom/client";
import { useState } from "react";
import store from "./store.js";

const Header = () => {
    const [text, setText] = useState("")
    const dispatch = useDispatch()

    const handleChange = e => setText(e.target.value)

    const handleKeyDown = e => {
        const trimmedText = e.target.value.trim()
        if (e.key === "Enter" && trimmedText) {
            dispatch({ type: "todos/added", payload: trimmedText })
            setText("")
            console.log(store.getState())
        }
    }

    return (
        <input
            type="text"
            placeholder="What needs to be done?"
            autoFocus={true}
            value={text}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
        />
    )
}

const TodoList = () => {
    const todoIdentifiers = useSelector(state => state.todos.map(todo => todo.id))

    const renderedListItems = todoIdentifiers.map(id => {
        return <TodoListItem key={id} id={id} />
    })

    return <ul className="todo-list">{renderedListItems}</ul>
}

const selectTodoById = (state, todoId) => {
    return state.todos.find(todo => todo.id == todoId)
}

const TodoListItem = ({ id }) => {
    const todo = useSelector(state => selectTodoById(state, id))
    const { text, completed, colour } = todo

    const dispatch = useDispatch()

    const handleCompletedChanged = () => {
        dispatch({ type: "todos/toggled", payload: todo.id })
    }

    return (
        <li>
            <div className="view">{text}</div>
        </li>
    )
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
    <Provider store={store}>
        <Header />
        <TodoList />
    </Provider>
)
