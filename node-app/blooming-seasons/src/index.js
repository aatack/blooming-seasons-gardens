import React from "react";
import { useSelector, useDispatch, Provider, shallowEqual } from "react-redux";
import ReactDOM from "react-dom/client";
import { useState } from "react";
import store from "./store.js";
import { colourOptionsElements } from "./features/filters.js"

const Header = () => {
    const [text, setText] = useState("")
    const dispatch = useDispatch()

    const handleChange = e => setText(e.target.value)

    const handleKeyDown = e => {
        const trimmedText = e.target.value.trim()
        if (e.key === "Enter" && trimmedText) {
            dispatch({ type: "todos/added", payload: trimmedText })
            setText("")
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
    const todoIdentifiers = useSelector(
        state => state.todos.map(todo => todo.id), shallowEqual
    )

    const renderedListItems = todoIdentifiers.map(id => {
        return <TodoListItem key={id} id={id} />
    })

    return <ul className="todo-list" style={{ listStyle: "none" }}>
        {renderedListItems}
    </ul>
}

const selectTodoById = (state, todoId) => {
    return state.todos.find(todo => todo.id === todoId)
}

const TodoListItem = ({ id }) => {
    const todo = useSelector(state => selectTodoById(state, id))

    const [completed, setCompleted] = useState(todo.completed)
    const [colour, setColour] = useState(todo.colour || "none")

    const dispatch = useDispatch()

    const handleCompletedChanged = (e) => {
        setCompleted(e.target.checked)
        dispatch({ type: "todos/toggled", payload: todo.id })
    }

    const handleColourChanged = e => {
        setColour(e.target.value)
        dispatch({
            type: "todos/colourChanged",
            payload: { id: todo.id, colour: e.target.value }
        })
    }

    const handleDeleted = () => {
        dispatch({ type: "todos/deleted", payload: todo.id })
    }

    return (
        <li>
            <div className="view">
                <input
                    type="checkbox"
                    checked={completed}
                    onChange={handleCompletedChanged}
                />
                {todo.text}
                <select value={colour} onChange={handleColourChanged}>
                    {colourOptionsElements}
                </select>
                <button onClick={handleDeleted}>Delete</button>
            </div>
        </li>
    )
}

const Footer = () => {
    const todosRemaining = useSelector(state => {
        return state.todos.filter(todo => !todo.completed).length
    })

    const { status, filters } = useSelector(state => state.filters)

    return (
        <footer className="footer">
            <div className="actions">
                <h5>Actions</h5>
                <button className="button">Mark all completed</button>
                <button className="button">Clear completed</button>
            </div>

            <p>{todosRemaining} items remaining</p>
            {/* <StatusFilter value={status} onChange={onStatusChange} />
            <ColourFilters value={colours} onChange={onColourChange} /> */}
        </footer>
    )
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
    <Provider store={store}>
        <Header />
        <TodoList />
        <Footer />
    </Provider>
)
