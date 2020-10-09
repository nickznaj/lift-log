import React, { Component } from 'react'
import NavLink from '../reusables/NavLink'
import './Header.css'

export default class Header extends Component {
    render() {
        return (
            <div className="header">
                <div>LOGO GOGO</div>
                <NavLink to="/calendar"> cal </NavLink>
                {this.props.children}
            </div>
        )
    }
}
