import { useContext, useState } from "react";
import colors from "../public/cta_data/theme.json";

import {
  LineColorsType,
  AppContext,
  AppContextType,
} from "../components/AppContext";
import Container from "../components/container";
import Header from "../components/header";
import FWLink from "../components/fw-link";
import clsx from "clsx";
import TrainIcon from "../public/icons/train.svg";
import CircleArrow from "../public/icons/circle-arrow.svg";
import l_stops from "../public/l-stops.json";
import cta_routes from "../public/cta_data/routes.json";

const SectionBox: React.FC<{ title: string }> = ({ children, title }) => (
  <div className="bg-grey my-2 pt-4">
    <h2 className="text-4xl tracking-tighter font-bold px-6 pb-4">{title}</h2>
    {children}
  </div>
);

const ChooseStop = () => {
  const context: AppContextType = useContext(AppContext);
  type Dir = "N" | "S" | "E" | "W" | undefined;
  const [state, setState] = useState(undefined);

  let style = {
    "--line": context.line ? colors[context.line] : "white",
  } as React.CSSProperties;

  type LBProps = { bgColor: LineColorsType };
  const LineBox = (props: LBProps) => {
    let style = { "--line": colors[props.bgColor] } as React.CSSProperties;
    return (
      <div
        style={style}
        className={clsx(
          "w-auto h-16 flex items-center bg-[color:var(--line)]",
          context.line == props.bgColor
            ? "border-4 border-white"
            : "border-none"
        )}
        onClick={() =>
          context.updateAppContext
            ? context.updateAppContext({
                ...context,
                line: props.bgColor,
                stop_name: undefined,
                stop_id: undefined,
              })
            : {}
        }
      >
        {context.line == props.bgColor ? (
          <TrainIcon className="mx-auto" />
        ) : (
          <p className="tracking-tight capitalize font-bold text-xl mx-auto">
            {props.bgColor}
          </p>
        )}
      </div>
    );
  };

  return (
    <Container>
      <Header />
      <h1 className="text-5xl tracking-tighter font-bold mx-6 my-12">
        Pick your stop
      </h1>
      <SectionBox title="Line">
        <div className="grid grid-cols-4 gap-0 ">
          <LineBox bgColor="red" />
          <LineBox bgColor="blue" />
          <LineBox bgColor="brown" />
          <LineBox bgColor="green" />
          <LineBox bgColor="orange" />
          <LineBox bgColor="pink" />
          <LineBox bgColor="purple" />
          <LineBox bgColor="yellow" />
        </div>
      </SectionBox>
      <SectionBox title="Stop">
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
      </SectionBox>
      <SectionBox title="Direction">
        <div className="grid grid-cols-2 w-auto border-black border-t-8">
          <button
            className={clsx(
              "pl-6 py-2 border-r-8 border-black text-left text-xl tracking-tight font-bold",
              "hover:bg-white hover:text-black"
            )}
            onClick={() =>
              context.updateAppContext && context.stop_name && context.line
                ? context.updateAppContext({
                    ...context,
                    stop_id: l_stops.filter(
                      (s) =>
                        s.STATION_NAME == context.stop_name &&
                        (s.DIRECTION_ID == "W" || s.DIRECTION_ID == "N")
                    )[0].STOP_ID,
                  })
                : {}
            }
          >
            <CircleArrow className="w-6 h-6 rotate-180 inline mr-2" />
            {context.stop_name && context.line
              ? `To ${cta_routes[context.line][0]}`
              : "Choose a stop"}
          </button>
          <button
            className="text-right pr-6 text-xl tracking-tight font-bold hover:bg-white hover:text-black"
            onClick={() =>
              context.updateAppContext && context.stop_name && context.line
                ? context.updateAppContext({
                    ...context,
                    stop_id: l_stops.filter(
                      (s) =>
                        s.STATION_NAME == context.stop_name &&
                        (s.DIRECTION_ID == "E" || s.DIRECTION_ID == "S")
                    )[0].STOP_ID,
                  })
                : {}
            }
          >
            {context.line && context.stop_name
              ? `To ${cta_routes[context.line].at(-1)}`
              : "Choose a stop"}
            <CircleArrow className="w-6 h-6 inline ml-2" />
          </button>
        </div>
      </SectionBox>
      <FWLink
        text={context.stop_id ? `Find a song!` : "Almost done..."}
        size="small"
        bgColor={context.line}
        href="/song"
      />
    </Container>
  );
};

export default ChooseStop;
