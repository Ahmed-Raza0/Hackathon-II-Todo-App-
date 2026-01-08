/**
 * TaskSkeleton component - loading placeholder for tasks
 * Displays animated skeleton loaders while tasks are being fetched
 */
export function TaskSkeleton() {
  return (
    <div className="space-y-3">
      {[1, 2, 3].map((i) => (
        <div
          key={i}
          className="bg-white rounded-lg p-4 shadow-sm border border-gray-200 animate-pulse"
        >
          <div className="flex items-center gap-3">
            {/* Checkbox skeleton */}
            <div className="h-5 w-5 bg-gray-200 rounded"></div>

            {/* Title skeleton */}
            <div className="flex-1">
              <div className="h-4 bg-gray-200 rounded w-3/4"></div>
              <div className="h-3 bg-gray-100 rounded w-1/4 mt-2"></div>
            </div>

            {/* Delete button skeleton */}
            <div className="h-8 w-8 bg-gray-200 rounded"></div>
          </div>
        </div>
      ))}
    </div>
  );
}
