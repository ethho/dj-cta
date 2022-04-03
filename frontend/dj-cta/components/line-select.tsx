import { useContext } from "react";
import { AppContext, LineColorsType } from "../components/AppContext";
import colors from "../public/cta_data/theme.json";
import clsx from "clsx";
import TrainIcon from "../public/icons/train.svg";

type LBProps = { bgColor: LineColorsType };

export const LineBox = (props: LBProps) => {
  let context = useContext(AppContext);
  let style = { "--line": colors[props.bgColor] } as React.CSSProperties;
  return (
    <div
      style={style}
      className={clsx(
        "w-auto h-16 flex items-center bg-[color:var(--line)]",
        context.line == props.bgColor ? "border-4 border-white" : "border-none"
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

export default function LineSelect() {
  return (
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
  );
}
