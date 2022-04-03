import CircleArrow from "../public/icons/circle-arrow.svg";
import clsx from "clsx";

type FWLinkProps = {
  text: string;
  bgColor?: string;
  href: string;
  size: "large" | "small";
};

const FWLink: React.FC<FWLinkProps> = (props) => (
  <div
    className={clsx(
      "py-4 px-6 mb-1 flex items-center",
      props.bgColor ? props.bgColor : "bg-grey"
    )}
  >
    <div>
      <a
        className={clsx(
          "font-bold tracking-tighter mt-8 pt-4 hover:underline underline-offset-8",
          props.size == "large" ? "text-3xl" : "text-2xl"
        )}
        href={props.href}
      >
        {props.text}
      </a>
    </div>
    <CircleArrow className="ml-auto w-6 h-6" />
  </div>
);

export default FWLink;
