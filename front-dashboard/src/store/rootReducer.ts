import { combineReducers } from '@reduxjs/toolkit';
import {profileReducer} from './reducers/profile'
import {DashboardReducer} from './reducers/dashboard'
import {monitorReducer} from "./reducers/monitor";

const rootReducer = combineReducers({
    profile: profileReducer,
    dashboard: DashboardReducer,
    monitor: monitorReducer
});

export type RootState = ReturnType<typeof rootReducer>;
export default rootReducer;
