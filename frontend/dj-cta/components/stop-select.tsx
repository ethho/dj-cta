import { useContext } from "react";
import { AppContext, LineColorsType } from "../components/AppContext";
import colors from "../public/cta_data/theme.json";
import clsx from "clsx";

import cta_routes from "../public/cta_data/routes.json";

export default function StopSelect() {
  let context = useContext(AppContext);
  let style = {
    "--line": context.line ? colors[context.line] : "white",
  } as React.CSSProperties;

  return (
    <div
      style={style}
      className={clsx(
        "mx-6 mt-4 border-l-[color:var(--line)] border-l-8",
        context.line ? "visible" : "hidden"
      )}
    >
      {context.line &&
        cta_routes[context.line]?.map((s, k) => (
          <div
            className={clsx(
              "ml-4 text-xl display-block",
              context.stop_name == s
                ? ""
                : "before:absolute before:ml-[-24px] before:mt-[9px] before:w-2 before:h-2 before:rounded-full before:bg-white"
            )}
            key={k}
          >
            <button
              onClick={() =>
                context.updateAppContext
                  ? context.updateAppContext({ ...context, stop_name: s })
                  : {}
              }
              className={clsx(
                "text-tight mb-2 text-xl",
                context.stop_name == s
                  ? "font-bold before:absolute before:ml-[-24px] before:mt-[9px] before:w-2 before:h-2 before:rounded-full before:border-2 before:border-black before:bg-white"
                  : "text-regular"
              )}
            >
              {s}
            </button>
          </div>
        ))}
    </div>
  );
}
