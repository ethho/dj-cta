import LogoIcon from "../public/icons/logo.svg";
import Link from "next/link";

export default function Header() {
  return (
    <nav className="flex items-center dark:text-white p-6">
      <Link href="/">
        <a>
          <LogoIcon />
        </a>
      </Link>
    </nav>
  );
}
