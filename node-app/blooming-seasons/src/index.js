import React from "react";
import ReactDOM from "react-dom/client";

function BoilingVerdict(props) {
    if (props.celsius >= 100) {
        return <p>The water would boil.</p>
    } else {
        return <p>The water would not boil.</p>
    }
}

class Calculator extends React.Component {
    constructor(props) {
        super(props);

        this.state = { temperature: "" };
    }

    handleChange = e => {
        this.setState({ temperature: e.target.value });
    }

    render() {
        return (
            <div>
                <TemperatureInput scale="c" />
                <TemperatureInput scale="f" />
            </div>
        )
    }
}

const scaleNames = {
    c: "Celsius",
    f: "Fahrenheit"
}

function toCelsius(fahrenheit) {
    return (fahrenheit - 32) * 5 / 9;
}

function toFahrenheit(celsius) {
    return (celsius * 9 / 5) + 32;
}

function tryConvert(temperature, convert) {
    const input = parseFloat(temperature);
    if (Number.isNaN(input)) {
        return '';
    }
    const output = convert(input);
    const rounded = Math.round(output * 1000) / 1000;
    return rounded.toString();
}

class TemperatureInput extends React.Component {
    constructor(props) {
        super(props);

        this.state = { temperature: "" };
    }

    handleChange = e => {
        this.setState({ temperature: e.target.value });
    }

    render() {
        const temperature = this.state.temperature;
        const scale = this.props.scale;

        return (
            <fieldset>
                <legend>Enter temperatre in {scaleNames[scale]}:</legend>
                <input value={temperature} onChange={this.handleChange} />
            </fieldset>
        )
    }
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<Calculator />)
