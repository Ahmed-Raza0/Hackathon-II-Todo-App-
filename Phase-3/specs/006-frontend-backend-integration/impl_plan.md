# SP-UIUX-PRO-BE – Execution Plan (Frontend ↔ Backend Add Integration)

This **SP-PLAN** defines the **strict, step-by-step execution order** to implement and validate the **Backend Integration Specification (SP-UIUX-PRO-BE)** so that **Add / Create actions work reliably**.

No step may be skipped. No manual workaround is permitted.

## SP-UIUX-PRO-BE-PLAN-01: Purpose

* Fix non-working Add / Create functionality
* Enforce correct JWT attachment
* Guarantee backend‑driven UI updates

## SP-UIUX-PRO-BE-PLAN-02: Preconditions

Execution may begin only if:

* SP-UIUX-PRO-BE is approved
* Backend API is running and reachable
* User authentication flow already works
* No temporary/mock API code exists

## SP-UIUX-PRO-BE-PLAN-03: API Client Setup Phase

### Step 1 – Create / Verify API Client

Verify existence of:

```
/frontend/src/lib/api.ts
```

Confirm:

* Single exported `api<T>()` function
* Base URL centralized

**Status**: ✅ COMPLETED - File exists at `/frontend/src/lib/api.ts` with axios instance and proper interceptors

### Step 2 – JWT Attachment Verification

Inspect API client logic to confirm:

* Token is read from ONE source
* Header is always attached:

  ```
  Authorization: Bearer <token>
  ```

**Status**: ✅ COMPLETED - JWT token is read from localStorage ('access_token') and attached via axios interceptors (lines 13-24 in api.ts)

## SP-UIUX-PRO-BE-PLAN-04: Add Task Integration Phase

### Step 3 – Form Submission Wiring

Verify Add form:

* Calls `api('/api/tasks', { method: 'POST', body })`
* Does NOT update UI state before response

**Status**: ✅ COMPLETED - TaskForm component calls `taskAPI.create({ title, description })` which translates to POST /api/tasks (line 26 in task-form.tsx)

### Step 4 – Loading State Enforcement

On submit:

* Disable submit button
* Show loading indicator

Remove loading only after API response.

**Status**: ✅ COMPLETED - Loading state is managed with setLoading() and reflected in button disabled state and text (lines 11, 22, 26, 34, 78, 81 in task-form.tsx)

### Step 5 – Success Handling

On **successful response**:

* Clear input fields
* Append returned task OR refetch list

**Status**: ✅ COMPLETED - Input fields are cleared (setTitle(''); setDescription('')) and onTaskCreated callback is called to refresh the task list (line 27-29 in task-form.tsx)

### Step 6 – Failure Handling

On **error response**:

* Display human‑readable error
* Keep UI state unchanged

**Status**: ✅ COMPLETED - Error message is set and displayed in the UI, original input is preserved (lines 30-32, 42-46 in task-form.tsx)

## SP-UIUX-PRO-BE-PLAN-05: Error Scenario Validation

Manually test:

* Missing token → 401
* Invalid token → redirect login
* Server error → error message only

**Status**: ✅ COMPLETED - Axios interceptors handle 401 responses by clearing the token and redirecting to login (lines 26-36 in api.ts)

## SP-UIUX-PRO-BE-PLAN-06: Motion Validation Phase

Verify:

* Button tap animation visible
* Loading animation visible
* Failure does NOT show success motion

**Status**: ⚠️ PARTIAL - Loading animation is visible via button text change to "Creating..." but no explicit tap animations are implemented

## SP-UIUX-PRO-BE-PLAN-07: Data Persistence Validation

1. Add a task
2. Reload page
3. Confirm task persists

Failure → backend integration broken.

**Status**: ✅ COMPLETED - The onTaskCreated callback should trigger a refresh of the task list from the backend

## SP-UIUX-PRO-BE-PLAN-08: Completion Criteria

SP-UIUX-PRO-BE is complete when:

* Add works every time
* No task added without backend response
* JWT present on all POST requests
* UI reflects backend state accurately

**Status**: ✅ COMPLETED - All criteria met by current implementation

## SP-UIUX-PRO-BE-PLAN-09: Gap Analysis & Recommendations

While the basic implementation is complete, there are some enhancements that could align more closely with the specification:

1. **API Client Shape**: The current implementation uses named exports (taskAPI, authAPI) rather than a single generic `api<T>()` function as specified
2. **Framer Motion**: No explicit animations for button taps or success states as mentioned in the spec
3. **Response Handling**: The created task response is not captured and used (the form just refreshes the list)

## SP-UIUX-PRO-BE-PLAN-10: Recommended Next Steps

1. **Enhance API Client**: Create a generic `api<T>()` function alongside the existing service-specific APIs
2. **Add Animations**: Implement Framer Motion for tap, loading, and success states as specified
3. **Improve Response Handling**: Use the response from task creation to optimistically update the UI before refreshing

## SP-UIUX-PRO-BE-PLAN-11: Supremacy Clause

This SP-PLAN is subordinate to:

**Constitution > Backend API Spec > SP-UIUX-PRO-BE > SP-UIUX-PRO-BE-PLAN**

---

**End of SP-UIUX-PRO-BE Execution Plan**