import React, { Component } from 'react';
import $ from 'jquery';

import '../stylesheets/CategoryView.css';

class CategoryView extends Component {
    constructor(props) {
        super();
        this.state = {
            categoryType: ""
        }
    }

    submitCategory = (event) => {
        event.preventDefault();
        $.ajax({
            url: '/categories',
            type: "POST",
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                categoryType: this.state.categoryType
            }),
            xhrFields: {
                withCredentials: true
            },
            crossDomain: true,
            success: (result) => {
                document.getElementById("add-category-form").reset();
                return;
            },
            error: (error) => {
                alert('Unable to add category. Please try your request again')
                return;
            }
        })
    }

    handleChange = (event) => {
        this.setState({[event.target.name]: event.target.value})
    }

    render() {
        return (
            <div id="add-category">
            <h2>Add a New Trivia Category</h2>
                <form className="form-view" id="add-category-form" onSubmit={this.submitCategory}>
            <label> Category
                <input type="text" name="categoryType" onChange={this.handleChange}/>
            </label>
            <input type="submit" className="button" value="Submit" />
            </form>
     </div>
    );
    }

}

export default CategoryView;