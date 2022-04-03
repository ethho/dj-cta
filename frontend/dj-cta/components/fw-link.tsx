import CircleArrow from "../public/icons/circle-arrow.svg";
import clsx from "clsx";
import Link from "next/link";

import colors from "../public/cta_data/theme.json";
import { LineColorsType } from "../components/AppContext";
import { CSSProperties } from "react";

type FWLinkProps = {
  text: string;
  bgColor?: LineColorsType;
  href: string;
  size: "large" | "small";
};

const FWLink: React.FC<FWLinkProps> = (props) => {
  let style = {
    "--line": props.bgColor ? colors[props.bgColor] : colors["grey"],
  } as CSSProperties;
  return (
    <div
      style={style}
      className={clsx(
        "py-4 px-6 mb-1 flex items-center",
        props.bgColor ? "bg-[color:var(--line)]" : "bg-grey"
      )}
    >
      <div>
        <Link href={props.href}>
          <a
            className={clsx(
              "font-bold tracking-tighter mt-8 pt-4 hover:underline underline-offset-8",
              props.size == "large" ? "text-3xl" : "text-2xl"
            )}
            href={props.href}
          >
            {props.text}
            <span className="ml-2">
              <CircleArrow className="ml-auto w-6 h-6 inline" />
            </span>
          </a>
        </Link>
      </div>
    </div>
  );
};

export default FWLink;
