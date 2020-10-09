import React, { Component } from 'react';
import CalendarView from './pages/CalendarView/CalendarView'
import SingleDayView from './pages/SingleDayView/SingleDayView'
import 'normalize.css'; 
import './App.css';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useRouteMatch,
  useParams
} from "react-router-dom";


export default class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      workout: {}
    }
  }

  
  render() {
    return (
      <div className="App">
        
        <Router>
          <div>
            <ul>
              <li>
                <Link to="/workouts">Home</Link>
              </li>
              <li>
                <Link to="/calendar">About</Link>
              </li>
            </ul>

            <Switch>
              <Route path="/calendar">
                <CalendarView />
              </Route>
              <Route path="/workouts/:date">
                <SingleDayView />
              </Route>
              <Route path="/workouts/">
                <SingleDayView />
              </Route>
              {/* <Route path="/">
                <Home /> */}
              {/* </Route> */}
            </Switch>
          </div>
        </Router>
      </div>
    )
  }
}
