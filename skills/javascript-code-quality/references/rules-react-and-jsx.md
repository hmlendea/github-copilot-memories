# JavaScript Rules: React And JSX

One directive per JavaScript rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Return a value from every React `render()` method.
- Enclose comments within JSX children in braces (`{/* comment */}`).
- Never let JSX conditions produce non-boolean values (`{count && <List />}`); convert the condition to a boolean (`{count > 0 && <List />}`).
- Call React Hooks only at the top level of function components and custom Hooks, never conditionally, in loops, or in nested functions.
- Delete unused methods of React components.
- Never call a `useState` setter directly in a component body or `render()`; call it from effects or event handlers.
- Never call a React state setter with its own state variable (`setCount(count)`).
- Provide a `key` property to every JSX element in a list or iterator.
- Never define React components within other components; define them at module level.
- Never use array indexes as JSX `key` values.
- Provide stable identities to React Context Provider values; memoise objects and functions with `useMemo()` or `useCallback()`.
- Use stable JSX keys; never generate them with `Math.random()`, `Date.now()`, or other per-call values.
- Never mutate `this.state` directly; use `setState()`.
- Use only recognised DOM properties and attributes in JSX (`className`, not `class`); no additional properties are permitted.
- Pass React `children` as nested JSX content, never as a `children` prop.
- Delete redundant JSX fragments (fragments with a single child or within an element).
- Never use the return value of `ReactDOM.render()`; use a callback ref.
- Destructure the `useState` return value into symmetrically named variables (`[count, setCount]`).
- Use the callback form of `setState()` (`setState(previousState => …)`) when the next state derives from the previous state.
- Never use `this` in function components.
- Never combine `children` with `dangerouslySetInnerHTML` on one element.
- Never define `shouldComponentUpdate()` in classes extending `React.PureComponent`.
- Escape JSX special characters (`>`, `"`, `'`, `}`) in text with HTML entities or expressions.
- Delete unused React prop type declarations.
- Name user-defined JSX components in Pascal case.
- Ensure spacing between inline JSX elements on separate lines is explicit (`{' '}`); JSX eliminates the line break.
- Declare `propTypes` for every prop a React component uses.
- Declare every prop in `defaultProps` as non-required in `propTypes`.
- Never use `ReactDOM.findDOMNode()`; use refs.
- Never use `isMounted()`; cancel pending operations in `componentWillUnmount()` or effect clean-up functions.
- Never use string refs; use callback refs, `createRef()`, or `useRef()`.
- Never use legacy React lifecycle methods (`componentWillMount`, `componentWillReceiveProps`, `componentWillUpdate`) or their `UNSAFE_` variants.
- Never use deprecated React APIs; migrate to their substitutes.
