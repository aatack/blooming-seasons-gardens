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

        this.state = { temperature: "0" };
    }

    onChange = value => {
        this.setState({ temperature: value });
    }

    render() {
        return (
            <div>
                <TemperatureInput
                    scale="c"
                    value={this.state.temperature}
                    onChange={this.onChange} />
                <TemperatureInput
                    scale="f"
                    value={this.state.temperature}
                    onChange={this.onChange} />
                <BoilingVerdict celsius={this.state.temperature} />
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
    }

    onChange = e => {
        this.props.onChange(
            this.props.scale === "c" ?
                e.target.value :
                tryConvert(e.target.value, toCelsius)
        );
    }

    render() {
        const scale = this.props.scale;
        const temperature = (
            scale === "c" ?
                this.props.value :
                tryConvert(this.props.value, toFahrenheit)
        );

        return (
            <fieldset>
                <legend>Enter temperature in {scaleNames[scale]}:</legend>
                <input value={temperature} onChange={this.onChange} />
            </fieldset>
        )
    }
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<Calculator />)
