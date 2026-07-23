import { Component, type ReactNode } from "react";

interface Props {
  children: ReactNode;
}
interface State {
  hasError: boolean;
}

export default class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError(): State {
    return { hasError: true };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error("Uncaught render error:", error, info);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex min-h-screen flex-col items-center justify-center gap-4 p-8 text-center">
          <h1 className="text-2xl font-semibold">Something went wrong</h1>
          <p className="text-gray-500">
            We hit an unexpected error. Try reloading the page.
          </p>
          <button
            onClick={() => window.location.reload()}
            className="rounded bg-black px-4 py-2 text-white"
          >
            Reload
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}