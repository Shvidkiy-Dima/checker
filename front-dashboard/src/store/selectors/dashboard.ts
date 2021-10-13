import { createSelector } from 'reselect'
import {RootState} from "../rootReducer";

export const selectMonitorIds = createSelector(
    (state: RootState)  => state.dashboard.monitors,
  monitors => Object.keys(monitors)
)



