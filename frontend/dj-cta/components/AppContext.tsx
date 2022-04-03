import { createContext } from "react";

export type LineColorsType =
  | "red"
  | "blue"
  | "brown"
  | "green"
  | "orange"
  | "pink"
  | "purple"
  | "yellow";

export type AppContextType = {
  line?: LineColorsType;
  stop_name?: string;
  stop_id?: number;
  updateAppContext?: (context: AppContextType) => void;
};

export const AppContext = createContext<AppContextType>({});
