import { createContext } from "react";

export type AppContextType = {
  line?:
    | "red"
    | "blue"
    | "brown"
    | "green"
    | "orange"
    | "pink"
    | "purple"
    | "yellow";
  stop_name?: string;
  stop_id?: string;
  setContext: (context: AppContextType) => void;
};

export const AppContext = createContext({
  setContext: (x: AppContextType) => {},
});
