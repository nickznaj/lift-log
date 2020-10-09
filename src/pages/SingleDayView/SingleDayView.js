import React, { Component } from 'react'
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link,
    useRouteMatch,
    useParams
} from "react-router-dom";

function SingleDayView() {
    let { date } = useParams()

    debugger

    return (
        <div>
            single day
        </div>
    )
}

export default SingleDayView