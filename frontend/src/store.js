import { createStore, compose, applyMiddleware, combineReducers } from "redux";
import thunk from "redux-thunk";
import { downloadDatasetReducer, downloadModelReducer } from "./reducers/downloadReducers";
import { aequitasRunReducer } from "./reducers/runReducers";
import { configCreateReducer, configUpdateReducer, fileSubmitReducer } from "./reducers/submitReducers";

const initialState = {
};

const reducer = combineReducers({
  fileSubmit: fileSubmitReducer,
  aequitasRunResult: aequitasRunReducer,
  downloadDataset: downloadDatasetReducer,
  downloadModel: downloadModelReducer,
  configCreate: configCreateReducer,
  configUpdate: configUpdateReducer,
})

const composeEnhancer = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

const store = createStore(
  reducer,
  initialState,
  composeEnhancer(applyMiddleware(thunk))
);

export default store;
