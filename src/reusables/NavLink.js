import React, { Component } from 'react'
import {Link} from 'react-router-dom'

export default class NavLink extends Component {
    constructor(props) {
        super(props)
    
        this.state = {
             
        }
    }
    
    render() {
        return (
            <div>
                <Link {...this.props}/> 
            </div>
        )
    }
}
