import {EMonitorActions} from "../../enums/actions.enum";
import {TMonitorAction} from "../../interfaces/monitor";

const initState: any = {
  id: null,
  interval_in_minutes: null,
  url: null,
  name: null,
  description: null,
  is_active: null,
  last_log: null,
  interval: null,
  next_request: null,
  successful_percent: null,
  unsuccessful_percent: null,
  last_request_in_seconds: null,
  created: null,
  error_notification_interval: null,
  error_notification_interval_in_minutes: null,
  by_telegram: null,
  by_email: null,
  max_timeout: null,
  avg_response_time: null,
  log_last_count: null,
  interval_logs: null,
  last_error_logs: null,
  log_groups: null,
  loaded: false,
  not_found: false,
  bar_data: [],
  table_data: [],
  chart_data: {},
};

const initialState = { ...initState };

export const monitorReducer = (state = initialState, action: TMonitorAction) => {
	switch (action.type) {
      case EMonitorActions.SetMonitor:
        return {
          ...state,
          ...action.payload,
          loaded: true,
          not_found: false,
        }
      case EMonitorActions.SetNotFound:
        return {
          ...state,
          not_found: action.payload,
        }

		default:
			return state;
	}
};