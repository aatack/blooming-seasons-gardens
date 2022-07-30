import React from "react";
import ReactDOM from "react-dom/client";

class NameForm extends React.Component {
    constructor(props) {
        super(props);

        this.state = { value: ["Initial text"] };
    }

    handleChange = (event) => {
        this.setState({ value: event.target.value });
    }

    handleSubmit = (event) => {
        alert("A name was submitted: " + this.state.value);
        event.preventDefault();
    }

    report = () => {
        alert("CLICKED")
    }

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <label>
                    Name:
                    <textarea value={this.state.value} onChange={this.handleChange} />
                </label>
                <select multiple={true} value={this.state.value} onChange={this.handleChange}>
                    <option value="red">Red</option>
                    <option value="blue">Blue</option>
                    <option value="yellow">Yellow</option>
                    <option value="green">Green</option>
                </select>
                <p onClick={this.report} hover="true">{this.state.value}</p>
                <input type="submit" />
                <input type="file" />
            </form>
        );
    }
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<NameForm />)
