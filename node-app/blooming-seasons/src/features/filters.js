function wrapFilter(filterReducer) {
    return (state, action) => {
        return { ...state, filters: filterReducer(state.filters, action.payload) }
    }
}

function statusChanged(state, payload) {
    return { ...state, status: payload }
}
