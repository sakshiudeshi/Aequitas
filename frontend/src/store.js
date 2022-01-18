import { createStore, compose, applyMiddleware, combineReducers } from "redux";
import thunk from "redux-thunk";
import { aequitasRunReducer } from "./reducers/runReducers";
import { fileSubmitReducer } from "./reducers/submitReducer";

const initialState = {};

const reducer = combineReducers({
  // upload dataset reducer needed
  fileSubmit: fileSubmitReducer,
  aequitasRunResult: aequitasRunReducer,
})

const composeEnhancer = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

const store = createStore(
  reducer,
  initialState,
  composeEnhancer(applyMiddleware(thunk))
);

export default store;
