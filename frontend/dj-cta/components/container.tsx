const Container: React.FC = ({ children }) => (
  <div className="dark:bg-black dark:text-white">
    <div className="max-w-screen-sm mx-auto min-h-screen">{children}</div>
  </div>
);

export default Container;
