import React from "react"

const initialState = {
    status: 'All',
    colours: []
}

export const colourOptions = {
    none: "None", red: "Red", yellow: "Yellow", green: "Green", blue: "Blue"
}

export const colourOptionsElements = []
for (const [key, value] of Object.entries(colourOptions)) {
    colourOptionsElements.push(<option value={key} key={key}>{value}</option>)
}

export default function filtersReducer(state = initialState, action) {
    switch (action.type) {
        case 'filters/statusChanged': {
            return {
                ...state, status: action.payload
            }
        }
        default:
            return state
    }
}